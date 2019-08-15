# -*- coding:utf-8 -*-

import argparse
import os

import cv2
import numpy

__author__ = 'LibX'


SSIM_DEFAULT_KERNEL=cv2.getGaussianKernel(11, 1.5)
SSIM_DEFAULT_WINDOW=SSIM_DEFAULT_KERNEL * SSIM_DEFAULT_KERNEL.T


def filter2valid(src, window):
    # https://cn.mathworks.com/help/matlab/ref/filter2.html#inputarg_shape
    ret = cv2.filter2D(src, -1, window, anchor=(1, 1), delta=0, borderType=cv2.BORDER_CONSTANT)
    return ret[1:ret.shape[0] - window.shape[0] + 2, 1:ret.shape[1] - window.shape[1] + 2]


def ssim_with_map(img1, img2, K=(0.01, 0.03), window=SSIM_DEFAULT_WINDOW, L=255, downsample=True):
    img1 = img1.astype(float)
    img2 = img2.astype(float)
    assert(img1.shape[0] == img2.shape[0] and img1.shape[1] == img2.shape[1])

    assert(len(K) == 2 and K[0] >= 0 and K[1] >= 0)

    M, N = img1.shape[0:2]
    H, W = window.shape[0:2]
    assert(H * W >= 4 and H <= M and W <= N)

    # automatic downsampling
    f = max(1, int(round(min(M, N) / 256.0)))
    # downsampling by f
    # use a simple low-pass filter
    if downsample and f > 1:
        lpf = numpy.ones((f, f))
        lpf = lpf / numpy.sum(lpf)

        # In opencv, filter2D use the center of kernel as the anchor,
        # according to http://docs.opencv.org/2.4.8/modules/imgproc/doc/filtering.html#void filter2D(InputArray src, OutputArray dst, int ddepth, InputArray kernel, Point anchor, double delta, int borderType)
        # but in matlab, imfilter use (2, 2) (matlab array starts with 1) as the anchor,
        # To ensure the results are the same with matlab's implementation, we set filter2D's anchor to (1, 1) (python array starts with 0)
        img1 = cv2.filter2D(img1, -1, lpf, anchor=(1, 1), borderType=cv2.BORDER_REFLECT)
        img2 = cv2.filter2D(img2, -1, lpf, anchor=(1, 1), borderType=cv2.BORDER_REFLECT)

        img1 = img1[0::f, 0::f]
        img2 = img2[0::f, 0::f]

    C1, C2 = tuple( (k * L) ** 2 for k in K)

    window = window / numpy.sum(window)

    mu1 = filter2valid(img1, window)
    mu2 = filter2valid(img2, window)

    mu1_sq = mu1 * mu1
    mu2_sq = mu2 * mu2

    mu1_mu2 = mu1 * mu2

    sigma1_sq = filter2valid(img1 * img1, window) - mu1_sq

    sigma2_sq = filter2valid(img2 * img2, window) - mu2_sq

    sigma12 = filter2valid(img1 * img2, window) - mu1_mu2

    ssim_map = ((2*mu1_mu2 + C1)*(2*sigma12 + C2))/((mu1_sq + mu2_sq + C1)*(sigma1_sq + sigma2_sq + C2))

    ssim_scalar = cv2.mean(ssim_map)

    return ssim_scalar[0], ssim_map


def ssim(img1, img2, K=(0.01, 0.03), window=SSIM_DEFAULT_WINDOW, L=255, downsample=True):
    ssim_val, ssim_map = ssim_with_map(img1, img2, K=K, window=window, L=L, downsample=downsample)
    return ssim_val


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose')
    parser.add_argument('--x', type=int)
    parser.add_argument('--y', type=int)
    parser.add_argument('--width', type=int)
    parser.add_argument('--height', type=int)
    parser.add_argument('--non-downsample', action='store_true', default=False, help='do not downsample')
    parser.add_argument('-m', '--ssim-map', action='store_true', default=False, help='show ssim map')
    parser.add_argument('-mh', '--ssim-map-histogram', action='store_true', default=False, help='show ssim map histogram')
    parser.add_argument('-mo', '--ssim-map-output', action='store_true', default=False, help='output ssim map')
    parser.add_argument('--ssim-map-output-base', help='ssim map output base')
    parser.add_argument('src_path')
    parser.add_argument('target_path')
    args = parser.parse_args()

    src_path = os.path.abspath(args.src_path)
    target_path = os.path.abspath(args.target_path)

    src_image = cv2.imread(src_path, cv2.IMREAD_GRAYSCALE)
    target_image = cv2.imread(target_path, cv2.IMREAD_GRAYSCALE)

    assert(src_image.shape[0] == target_image.shape[0] and src_image.shape[1] == target_image.shape[1])

    x = args.x if args.x is not None else 0
    y = args.y if args.y is not None else 0
    width = args.width if args.width is not None else (src_image.shape[1] - x)
    height = args.height if args.height is not None else (src_image.shape[0] - y)

    src_image = src_image[y:y+height, x:x+width]
    target_image = target_image[y:y+height, x:x+width]

    ssim_val, ssim_map = ssim_with_map(src_image, target_image, downsample=(not args.non_downsample))
    print ssim_val

    ssim_map_output_base = None
    if args.ssim_map_output:
        ssim_map_output_base = args.ssim_map_output_base
        if not ssim_map_output_base:
            ssim_map_output_base = os.path.dirname(target_path)

        if not os.path.exists(ssim_map_output_base):
            os.makedirs(ssim_map_output_base)

    if args.ssim_map or args.ssim_map_histogram:
        from matplotlib import pyplot as plt
        new_figure = False
        has_figure = False

        if args.ssim_map:
            # ssim map
            ssim_map_4 = numpy.floor(numpy.power(ssim_map, 4) * 255)

            # ssim map output
            if args.ssim_map_output:
                ssim_map_filename = os.path.basename(target_path)
                ssim_map_filename = '_ssimmap'.join(os.path.splitext(ssim_map_filename))
                ssim_map_filepath = os.path.join(ssim_map_output_base, ssim_map_filename)

                cv2.imwrite(ssim_map_filepath, ssim_map_4)
            else:
                # ssim map
                plt.imshow(ssim_map_4, cmap='gray')
                plt.title('ssim map')
                new_figure = True
                has_figure = True

        if args.ssim_map_histogram:
            # ssim map histogram
            # TODO implemnt output ssim map histogram
            if new_figure:
                plt.figure()

            ssim_map_array = ssim_map.reshape((1, ssim_map.shape[0] * ssim_map.shape[1]))[0]
            ssim_map_bins = [i / 100.0 for i in xrange(0, 101, 5)]
            plt.hist(ssim_map_array, bins=ssim_map_bins, normed=True)
            plt.title('ssim map histogram')
            new_figure = True
            has_figure = True

        if has_figure:
            plt.show()


if __name__ == '__main__':
    main()
