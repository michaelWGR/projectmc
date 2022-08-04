
def cal(total_value, rate_to_value):
    sum_total_value = sum(float(tv) for tv in total_value)
    if sum_total_value < 0:
        print('total_value must be bigger than 0')
        return
        
    if sum(float(k) for k in rate_to_value.keys()) != 1:
        print('sum rate must be 1')
        return
    
    handle_result = {}
    for k in rate_to_value:
        expect_value = float(sum_total_value) * k
        actual_value = sum(float(v) for v in rate_to_value[k])
        handle_value = expect_value - actual_value
        handle_result[k] = {'expect_value': expect_value,
                            'actual_value': actual_value,
                            'handle_value': handle_value}
    return handle_result


if __name__ == '__main__':
    """
    现金：0.1
    基金：0.39
    自选：0.37
    国债：0.14
    """
    total_value_list = [93585, 10572]
    rate_to_value_dict = {
        0.1: [10572],
        0.39: [14148, 18311],
        0.37: [7230, 1638, 981, 2784, 2074, 2400, 4762, 3808, 3724, 11121],
        0.14: [16000]}
    result = cal(total_value_list, rate_to_value_dict)
    for r in result:
        format_str = 'rate: {}, expect_value: {}, actual_value: {}, handle_value: {}'
        print(format_str.format(r, result[r]['expect_value'], result[r]['actual_value'], result[r]['handle_value']))
    
    
    