
runners = 6

start = 1
end = 0
for i in range(1, runners + 1):
    end = 255//runners*i
    if i == runners:
        end = 255
    
    
    print(start, end)

    start += (255//runners)
    