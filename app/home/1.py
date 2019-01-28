import random

def xier_sort(list):
    if len(list)<=1:
        return list
    else:
        length=len(list)
        group_num=length//2
        while group_num > 0:
            for i in range(group_num,length):
                current_index_value = list[i]
                k=i
                while k>=group_num and list[k-group_num]>current_index_value:
                    list[k]=list[k-group_num]
                    k-=group_num
                list[k]=current_index_value
            group_num=group_num//2
        return list
a=[]
for i in range(1,50):
    b = random.randint(1,100)
    while b in a:
        b = random.randint(1,100)
    a.append(b)

print(a)

