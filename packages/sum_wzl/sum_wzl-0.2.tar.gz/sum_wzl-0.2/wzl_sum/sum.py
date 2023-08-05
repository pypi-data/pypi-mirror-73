class Sum_obj:
    def __init__(self, begin, end):
        self._begin = begin
        self._end = end
        self._sum = 0

    def cal_sum(self,):
        tmp_sum = 0
        for i in range(self._begin, self._end+1):
            tmp_sum += i
        self._sum = tmp_sum
        return tmp_sum

    def get_sum(self):
        return self._sum

if __name__ == "__main__":
    sum_obj = Sum_obj(1, 3)
    res = sum_obj.cal_sum()
    res1 = sum_obj.get_sum()
    print("cal sum is " + str(res))
    print("get sum is " + str(res1))

