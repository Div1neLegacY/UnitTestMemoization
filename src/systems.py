if __name__ == '__main__':
    i = 0
    import time
    while True:
        time.sleep(0.5)

        if i == 10:
            break

        print(f"i={i}, ")
        i += 1

    print("Subprocess ending...")