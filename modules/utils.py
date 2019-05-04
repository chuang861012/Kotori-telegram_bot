def parse_book_result(arr,string):
    if arr == ['error : web request error']:
        return 'error : web request error'
    else:
        count=0
        for i in arr:
            if count==5:
                break
            else:
                string += "[{}]({}) - {} 元\n".format(i[0],i[1],i[2])
                count = count+1
        return string