def sort012(arr):
    #to store count
    cnt = {0:0,1:0,2:0}
    for i in arr:
        cnt[i] += 1

    #change arr according to count
    for index in range(len(arr)):
        if cnt[0]>0:
            arr[index]=0
            cnt[0]-=1
            continue
        elif cnt[1]>0:
            arr[index]=1
            cnt[1]-=1
            continue
        elif cnt[2]>0:
            arr[index]=2
            cnt[2]-=1
            continue
        else:
            break



arr = [0,1,1,1,2,0,2]
sort012(arr)
print(arr)