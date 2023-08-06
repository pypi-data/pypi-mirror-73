def get_file_size(file_path):
    '''
    os.path.getsize(filepath) 返回的是字节大小
    1Byte = 8bit
    1KB = 1024Byte
    1MB = 1024KB
    1GB = 1024MB
    根据文件大小，可以自适应显示文件的大小
    :param file_path:
    :return:size, unit
    '''
    unit = None
    if '/' in file_path:
        filename = file_path.split('/')[-1]
    if '\\' in file_path:
        filename = file_path.split('\\')[-1]
    size = os.path.getsize(file_path)
    if size < 1024:
        print('The %s size is : %dByte'%(filename, size))
        unit = 'Byte'
    if size > 1024 and size < 1024*1024:
        size = size / 1024
        print('The %s size is : %.2fKB' % (filename, size))
        unit = 'KB'
    if size >1024*1024 and size < 1024*1024*1024:
        size = size / (1024*1024)
        print('The %s size is : %.2fMB' % (filename, size))
        unit = 'MB'
    if size >1024*1024*1024 and size < 1024*1024*1024*1024:
        size = size / (1024*1024*1024)
        print('The %s size is : %.2fGB' % (filename, size))
        unit = 'GB'
    # print(size, unit)
    return size, unit




if __name__ == '__main__':
    file_path = r'D:\ZF\2_ZF_data\blad.zip'
    get_file_size(file_path)