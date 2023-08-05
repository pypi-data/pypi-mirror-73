class Sum_obj:
    def __init__(self, begin, end):
        self._begin = begin
        self._end = end
        self._sum = 0

    def cal_sum(self, begin,end):
        tmp_sum = 0
        for i in range(begin,end+1):
            tmp_sum += i
        self.sum = tmp_sum
        return tmp_sum

if __name__ == "__main__":
    sum_obj = Sum_obj(0, 100)
    res = sum_obj.cal_sum(sum_obj._begin, sum_obj._end)
    print("sum is " + str(res))

