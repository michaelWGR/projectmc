# -*- coding:utf-8 -*-

import json

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from forms import PaginatorForm
from enums import GameType, Hero
from models import *
from utils import JsonApi, JsonApiResponse


# Create your views here.


def resource_index(request):
    page_form = PaginatorForm(request.GET)
    page_form.is_valid()
    checked = request.GET.get('checked')
    print checked

    page_num = page_form.cleaned_data['page_num']
    page_size = page_form.cleaned_data['page_size']

    if page_size < 20:
        page_size = 2
    if page_size > 50:
        page_size = 2

    try:
        resources = Resource.objects.values('id', 'path', 'type', 'business_type', 'value', 'checked', 'ctime').filter(
            type=0).order_by('-id')
        if checked == 'finished':
            resources = resources.filter(checked=100).order_by('-id')
        elif checked == 'unfinished':
            resources = resources.filter(checked__lt=100).order_by('-id')
        else:
            checked = 'all'
        paginator = Paginator(resources, page_size)
        current_page = paginator.page(page_num)
    except Exception as e:
        return

    max_page_num = paginator.num_pages if paginator.num_pages < 5 else 5
    show_page_num = paginator.num_pages if paginator.num_pages < 5 else 5

    if current_page.number > max_page_num:
        max_page_num += current_page.number
        if max_page_num > paginator.num_pages:
            max_page_num = paginator.num_pages
    elif current_page.number < max_page_num and current_page.number > show_page_num:
        max_page_num -= show_page_num;

    page_list = list()

    if current_page.number <= show_page_num:
        for i in range(1, max_page_num + 1):
            page_list.append(i)
    else:
        page_list.append(1)
        for i in range(current_page.number - 3, current_page.number + 1):
            page_list.append(i)

    if paginator.num_pages > 10 and current_page.number != paginator.num_pages:
        page_list.append(paginator.num_pages)

    data = {
        'resources': current_page.object_list,
        'paginator': paginator,
        'checked': checked,
        'current_page': current_page,
        'page_list': page_list,
        'page_type': 'resource_index'
    }

    return render_to_response('management/resource/index.html', data)


def plist(request):
    page_number = 20
    filter_value = ""
    pid = None
    if "pid" in request.GET:
        pid = int(request.GET["pid"])
    if "page" not in request.GET:
        page = 1
    else:
        try:
            page = int(request.GET["page"])
        except ValueError:
            page = 1
        if page <= 0:
            page = 1
    if 'filterValue' in request.COOKIES:
        filter_value = request.COOKIES["filterValue"]
    if pid:
        sub_sql = 'SELECT `resources`.`id` FROM `resources` WHERE `resources`.`pid` = {}'.format(pid)
    else:
        sub_sql = 'SELECT `resources`.`id` FROM `resources` WHERE NOT(`resources`.`pid` = 0)'
    if filter_value != "":
        sub_sql += ' and value="{}"'.format(filter_value)
    sql = 'select * from resources join ({} ORDER BY `resources`.`id` DESC LIMIT {} OFFSET {}) as b using(id)'.format(
        sub_sql, page_number, page_number * (page - 1))
    db_data = Resource.objects.raw(sql)
    return render_to_response('management/resource/list.html',
                              {
                                  "data": db_data,
                                  "index": page, "page_type": "plist", "filter": filter_value, "pid": pid
                              })


def resource_checker(request, resource_id):
    data = {'resource_id': resource_id}
    v_resource = Resource.objects.get(pk=resource_id)

    # 只接受视频类型的资源处理请求
    if v_resource.type != 0:
        return render_to_response('management/resource/checker/blank.html')

    data['resource_path'] = v_resource.path

    # 1. 获取对应的 resource_id 下的所有 resource
    resources = Resource.objects.filter(pid=resource_id)
    _resources = []
    for resource in resources:
        _resources.append(model_to_dict(resource))
    data["child_resources"] = json.dumps(_resources)

    if v_resource.business_type == 0:
        return render_to_response('management/resource/checker/porn_checker.html', data)
    elif v_resource.business_type == 2:
        if v_resource.col_int_01 == GameType.quanjunchuji.value:
            return render_to_response('management/resource/checker/qjcj_game_checker.html', data)
        elif v_resource.col_int_01 == GameType.cijizhanchang.value:
            return render_to_response('management/resource/checker/cjzc_game_checker.html', data)
        elif v_resource.col_int_01 == GameType.juediqiusheng.value:
            return render_to_response('management/resource/checker/jdqs_game_checker.html', data)
        elif v_resource.col_int_01 == GameType.huangyexingdong.value:
            return render_to_response('management/resource/checker/hyxd_game_checker.html', data)
        elif v_resource.col_int_01 == GameType.wangzherongyao.value:
            heros = []
            for h in Hero:
                heros.append({"name": h.name, "value": h.value})
            data["heros"] = sorted(heros, key=lambda k: k['name'])
            return render_to_response('management/resource/checker/wzry_game_checker.html', data)
    else:
        return render_to_response('management/resource/checker/blank.html')


def resource_review(request, review_id):
    data = {"review_id": review_id}

    try:
        temp_review = TempReview.objects.get(id=review_id)
    except ObjectDoesNotExist:
        temp_review = None

    if temp_review:
        try:
            porn_result = PornResult.objects.get(product="ksyun", resource__id=temp_review.resource_id)
        except ObjectDoesNotExist:
            porn_result = None
        if not porn_result:
            return JsonApiResponse(1, 'fail', result="Can't get porn result, review_id: {}".format(review_id))

        try:
            resource = Resource.objects.get(id=temp_review.resource_id)
        except ObjectDoesNotExist:
            resource = None
        if not resource:
            return JsonApiResponse(1, 'fail', result="Can't get resource, review_id: {}".format(review_id))

        data["resource"] = resource
        data["porn_result"] = porn_result
        data["temp_review"] = temp_review

        try:
            next_need_temp_review = TempReview.objects.order_by("id").filter(id__gt=review_id, review_status=2)[:1][0]
        except IndexError:
            next_need_temp_review = None

        try:
            t = TempReview.objects.order_by("id").filter(id__gt=review_id)[:10]
            next_temp_review = t[0]
            l = len(t) - 1 if len(t) - 1 >= 0 else 0
            next_10_temp_review = t[l]
        except IndexError:
            next_temp_review = None
            next_10_temp_review = None

        try:
            t = TempReview.objects.order_by("-id").filter(id__lt=review_id)[:10]
            pre_temp_review = t[0]
            l = len(t) - 1 if len(t) - 1 >= 0 else 0
            pre_10_temp_review = t[l]
        except IndexError:
            pre_temp_review = None
            pre_10_temp_review = None

        data["next_need_review_id"] = next_need_temp_review.id if next_need_temp_review else -1
        data["next_review_id"] = next_temp_review.id if next_temp_review else review_id
        data["pre_review_id"] = pre_temp_review.id if pre_temp_review else 1
        data["next_10_review_id"] = next_10_temp_review.id if next_10_temp_review else review_id
        data["pre_10_review_id"] = pre_10_temp_review.id if pre_10_temp_review else 1
    else:
        return JsonApiResponse(1, 'fail', result="Can't get need temp_review object, id: {}".format(review_id))

    return render_to_response('management/resource/checker/pic_review.html', data)


@csrf_exempt
@JsonApi(permitted_methods=('POST',))
def batch_update_value(request):
    data = json.loads(request.body)["data"]
    r_id = json.loads(request.body)["resourceId"]

    if not data:
        return JsonApiResponse(1, 'fail', result="data is null")

    for k, v in data.items():
        value = None if k == 'null' else k
        ids = v

        Resource.objects.filter(id__in=ids).update(value=value)
        Resource.objects.filter(pid__in=ids).update(value=value)

    # 计算当前提交的结果打了标签的百分比
    resources = Resource.objects.filter(pid=r_id)
    count = 0
    for r in resources:
        if r.value is not None:
            count += 1

    r = Resource.objects.get(id=r_id)
    r.checked = int(count / float(len(resources)) * 100)
    r.save()

    return JsonApiResponse(0, 'succeed', result=123)


@csrf_exempt
@JsonApi(permitted_methods=('POST',))
def batch_update_json(request):
    data = json.loads(request.body)["data"]
    r_id = json.loads(request.body)["resourceId"]

    if not data:
        return JsonApiResponse(1, 'fail', result="data is null")

    for d in data:
        Resource.objects.filter(id__in=d["ids"]).update(col_json_01=json.dumps(d["info"]))

    # 计算当前提交的结果打了标签的百分比
    resources = Resource.objects.filter(pid=r_id)
    count = 0
    for r in resources:
        if r.col_json_01 is not None:
            count += 1

    r = Resource.objects.get(id=r_id)
    r.checked = int(count / float(len(resources)) * 100)
    r.save()
    return JsonApiResponse(0, 'succeed', result=123)


@csrf_exempt
@JsonApi(permitted_methods=('POST',))
def review_update(request):
    try:
        data = json.loads(request.body)["data"]
        resource_id = data["resourceId"]
        review_id = data["reviewId"]
        resource_old_value = data["resourceOldValue"]
        resource_new_value = data["resourceNewValue"]

        # update resource value
        r = Resource.objects.get(pk=resource_id)
        r.value = resource_new_value
        r.save()

        # update temp review
        tr = TempReview.objects.get(pk=review_id)
        tr.old_value = resource_old_value
        tr.new_value = resource_new_value
        tr.review_status = 3
        tr.save()

        return JsonApiResponse(0, 'succeed', result=123)
    except Exception as e:
        print e
        return JsonApiResponse(1, 'fail', result="Update error.")
