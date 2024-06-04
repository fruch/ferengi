CLUSTER_SIZE = 32768

file_num = 1
in_filename = "/home/fruch/sd-card-copy.img"

read_file = open(in_filename, 'rb')

found_pic = False
i = 0
write_file = None

while True:
    i = i + 1

    cluster = read_file.read(CLUSTER_SIZE)
    if bytes.fromhex("ffd8ffe1") in cluster:
        print(cluster[0:8].hex())
        print("found on: " + str(i))
        write_file = open( "Pic_"+str(file_num)+".JPG", 'wb')
        file_num = file_num + 1
        found_pic = True

    if found_pic:
       write_file.write(cluster)

    if len(cluster) < CLUSTER_SIZE:
        print("end.")
        break

read_file.close()
write_file.close()
