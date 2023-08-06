#Math
class Math:

    def addition(self, num_list):
        sum = 0
        for i in num_list:
            if type(i) == type(1) or type(i) == type(1.1):
                sum += i
            else:
                raise TypeError("Only integers or floats are allowed.")
        return sum

    def multiplication(self, a,b):
        return a*b

    def division(self, a,b):
        return a/b

    def subtraction(self, a,b):
        return a-b

Math = Math()
