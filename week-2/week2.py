#第一題
def calculate(min, max, step):
  sum = 0
  for x in range(min,max+1,step):
    sum = sum+x
  return print(sum)

calculate(1, 3, 1) # 你的程式要能夠計算 1+2+3，最後印出 6
calculate(4, 8, 2) # 你的程式要能夠計算 4+6+8，最後印出 18
calculate(-1, 2, 2) # 你的程式要能夠計算 -1+1，最後印出 0

#第二題
def avg(data):
  sum=0
  for i in range(0,4,1):
    if data["employees"][i]["manager"] is False:
      sum = sum + data["employees"][i]["salary"]
      
      
  count = 0
  for i in range(0,4,1):
    if data["employees"][i]["manager"] is False:
      count = i
      
  print(sum/count)

avg({
"employees":[
{
"name":"John",
"salary":30000,
"manager":False
},
{
"name":"Bob",
"salary":60000,
"manager":True
},
{
"name":"Jenny",
"salary":50000,
"manager":False
},
{
"name":"Tony",
"salary":40000,
"manager":False
}
]
}) # 呼叫 avg 函式

#第三題
def func(a):
    def function(b, c):
      print(a+(b*c))
    return function
func(2)(3, 4) # 你補完的函式能印出 2+(3*4) 的結果 14
func(5)(1, -5) # 你補完的函式能印出 5+(1*-5) 的結果 0
func(-3)(2, 9) # 你補完的函式能印出 -3+(2*9) 的結果 15
# 一般形式為 func(a)(b, c) 要印出 a+(b*c) 的結果

#第四題
def maxProduct(nums):
  
  sortedNums = sorted(nums, reverse=True)  # [5, 20, 2, 6]

  largestNums = sortedNums[0]  # 20
  secondLargestNums = sortedNums[1]  # 6

  smallestNums = sortedNums[-1]
  secondSmallestNums = sortedNums[-2]

  if largestNums * secondLargestNums > smallestNums * secondSmallestNums:
    print(largestNums * secondLargestNums)
  else:
    return print(smallestNums * secondSmallestNums)


maxProduct([5, 20, 2, 6]) # 得到 120
maxProduct([10, -20, 0, 3]) # 得到 30
maxProduct([10, -20, 0, -3]) # 得到 60
maxProduct([-1, 2]) # 得到 -2
maxProduct([-1, 0, 2]) # 得到 0
maxProduct([5,-1, -2, 0]) # 得到 2
maxProduct([-5, -2]) # 得到 10

#第五題
def twoSum(nums, target):
  for i, num in enumerate(nums):
        for j in range(i + 1, len(nums)):
            if num + nums[j] == target:
                return [i, j]

result=twoSum([2, 11, 7, 15], 9)
print(result) # show [0, 2] because nums[0]+nums[2] is 9