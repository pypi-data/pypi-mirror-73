import os
import meteva
import matplotlib.colors as colors
import time
from meteva.base.io.GDS_data_service import GDSDataService
from meteva.base.io import DataBlock_pb2
from multiprocessing import freeze_support,Process,cpu_count



def copy_data_one_cup(k,file_list,len_input,to_dir,input_fun,output_fun,rm_follow,ad_follow,effectiveNum,recover,grid):
    start = time.time()
    copyed_num = 0
    file_num = len(file_list)
    for i in range(file_num):
        file = file_list[i]
        path_input = file.replace("\\", "/")
        path_file = path_input[len_input:]
        path_output = to_dir + path_file
        filename,follow = os.path.splitext(path_output)
        if follow == rm_follow:
            path_output = filename
        path_output = path_output + ad_follow

        if not os.path.exists(path_output) or recover:
            meteva.base.tool.path_tools.creat_path(path_output)
            grd = input_fun(path_input,grid = grid)
            if grd is not None:
                output_fun(grd, path_output, effectiveNum)
                end = time.time()
                copyed_num += 1
                left_minutes = int((end - start) * (file_num - i - 1) / (copyed_num * 60)) + 1
                print("第"+str(k)+"个进程剩余" + str(left_minutes) + "分钟")
                # print(path_output)


def copy_data(input_root_dir,output_root_dir,input_type,output_type,effectiveNum = 3,recover= False,grid = None,cpu_num = 1):
    freeze_support()
    input_root_dir = input_root_dir.replace("\\","/")
    output_root_dir = output_root_dir.replace("\\","/")
    if input_root_dir[-1] != "/":
        input_root_dir += "/"
    if output_root_dir[-1] != '/':
        output_root_dir += "/"
    (gds_dir,file_model) = os.path.split(input_root_dir)
    from_dir = input_root_dir
    to_dir = output_root_dir
    file_list = meteva.base.tool.path_tools.get_path_list_in_dir(gds_dir)
    file_num = len(file_list)
    pro_num = cpu_count() - 2
    if cpu_num > cpu_num:
        pro_num = cpu_num
    file_dict_list = {}
    for i in range(pro_num):
        file_dict_list[i] = []
    for i in range(file_num):
        k = i % pro_num
        file_dict_list[k].append(file_list[i])

    input_fun = None
    rm_follow = ""
    if input_type == "m4":
        input_fun = meteva.base.read_griddata_from_micaps4
    elif input_type == "nc":
        input_fun = meteva.base.read_griddata_from_nc
        rm_follow ="nc"

    output_fun = None
    ad_follow = ""
    if output_type == "m4":
        output_fun = meteva.base.write_griddata_to_micaps4
    elif output_type == "nc":
        output_fun = meteva.base.write_griddata_to_nc
        ad_follow = ".nc"
    len_input = len(input_root_dir)
    PP = []
    for k in range(pro_num):
        tmpp = Process(target=copy_data_one_cup, args=(k,file_dict_list[k],len_input,to_dir,input_fun,output_fun,rm_follow,ad_follow,effectiveNum,recover,grid))
        PP.append(tmpp)
    print('Waiting for all subprocesses done...')
    for pc in PP:
        pc.start()

    for pp in PP:
        pp.join()
    print('All subprocesses done.')


def copy_m4_to_nc(input_root_dir,output_root_dir,effectiveNum = 3,recover= False,grid = None):
    input_root_dir = input_root_dir.replace("\\","/")
    output_root_dir = output_root_dir.replace("\\","/")
    if input_root_dir[-1] != "/":
        input_root_dir += "/"
    if output_root_dir[-1] != '/':
        output_root_dir += "/"
    (gds_dir,file_model) = os.path.split(input_root_dir)
    save_dir = output_root_dir
    file_list = meteva.base.tool.path_tools.get_path_list_in_dir(gds_dir)
    len_input = len(input_root_dir)
    file_num = len(file_list)
    start = time.time()
    copyed_num = 0

    for i in range(file_num):
        file = file_list[i]
        path_input = file.replace("\\","/")
        path_file = path_input[len_input:]
        path_output = output_root_dir + path_file+".nc"
        if not os.path.exists(path_output) or recover:
            meteva.base.tool.path_tools.creat_path(path_output)
            if grid is None:
                grd = meteva.base.io.read_griddata_from_micaps4(path_input)
            else:
                grd = meteva.base.io.read_griddata_from_micaps4(path_input,grid=grid)
            if grd is not None:
                meteva.base.io.write_griddata_to_nc(grd,path_output,effectiveNum)
                end = time.time()
                copyed_num +=1
                left_minutes = int((end - start) * ( file_num - i -1) / (copyed_num * 60)) + 1
                print("剩余" + str(left_minutes) + "分钟")
                #print(path_output)



def copy_gds_to_nc(input_root_dir,output_root_dir,effectiveNum = 3,recover= False,grid = None):
    input_root_dir = input_root_dir.replace("\\","/")
    output_root_dir = output_root_dir.replace("\\","/")
    if input_root_dir[-1] != "/":
        input_root_dir += "/"
    if output_root_dir[-1] != '/':
        output_root_dir += "/"
    (gds_dir,file_model) = os.path.split(input_root_dir)
    save_dir = output_root_dir
    file_list = meteva.base.tool.path_tools.get_path_list_in_dir(gds_dir)
    len_input = len(input_root_dir)
    file_num = len(file_list)
    start = time.time()
    copyed_num = 0
    for i in range(file_num):
        file = file_list[i]
        path_input = file.replace("\\","/")
        path_file = path_input[len_input:]
        path_output = output_root_dir + path_file+".nc"
        if not os.path.exists(path_output) or recover:
            meteva.base.tool.path_tools.creat_path(path_output)
            if grid is None:
                grd = meteva.base.io.read_griddata_from_gds_file(path_input)
            else:
                grd = meteva.base.io.read_griddata_from_gds_file(path_input,grid=grid)
            if grd is not None:
                meteva.base.io.write_griddata_to_nc(grd,path_output,effectiveNum)
                end = time.time()
                copyed_num +=1
                left_minutes = int((end - start) * ( file_num - i -1) / (copyed_num * 60)) + 1
                print("剩余" + str(left_minutes) + "分钟")
                print(path_output)


def copy_gds_to_m4(input_root_dir,output_root_dir,effectiveNum = 3,recover= False,grid = None):
    input_root_dir = input_root_dir.replace("\\","/")
    output_root_dir = output_root_dir.replace("\\","/")
    if input_root_dir[-1] != "/":
        input_root_dir += "/"
    if output_root_dir[-1] != '/':
        output_root_dir += "/"
    (gds_dir,file_model) = os.path.split(input_root_dir)
    save_dir = output_root_dir
    file_list = meteva.base.tool.path_tools.get_path_list_in_dir(gds_dir)
    len_input = len(input_root_dir)
    file_num = len(file_list)
    start = time.time()
    copyed_num = 0
    for i in range(file_num):
        file = file_list[i]
        path_input = file.replace("\\","/")
        path_file = path_input[len_input:]
        path_output = output_root_dir + path_file
        if not os.path.exists(path_output) or recover:
            meteva.base.tool.path_tools.creat_path(path_output)
            if grid is None:
                grd = meteva.base.io.read_griddata_from_gds_file(path_input)
            else:
                grd = meteva.base.io.read_griddata_from_gds_file(path_input,grid=grid)
            if grd is not None:
                meteva.base.io.write_griddata_to_micaps4(grd,path_output,effectiveNum = effectiveNum)
                end = time.time()
                copyed_num +=1
                left_minutes = int((end - start) * ( file_num - i -1) / (copyed_num * 60)) + 1
                print("剩余" + str(left_minutes) + "分钟")
                print(path_output)



def copy_wind_gds_to_nc(input_root_dir,output_root_dir,effectiveNum = 3,recover= False,grid = None):
    input_root_dir = input_root_dir.replace("\\","/")
    output_root_dir = output_root_dir.replace("\\","/")
    if input_root_dir[-1] != "/":
        input_root_dir += "/"
    if output_root_dir[-1] != '/':
        output_root_dir += "/"
    (gds_dir,file_model) = os.path.split(input_root_dir)
    save_dir = output_root_dir
    file_list = meteva.base.tool.path_tools.get_path_list_in_dir(gds_dir)
    len_input = len(input_root_dir)
    file_num = len(file_list)
    start = time.time()
    copyed_num = 0
    for i in range(file_num):
        file = file_list[i]
        path_input = file.replace("\\","/")
        path_file = path_input[len_input:]
        path_output = output_root_dir + path_file+".nc"
        if not os.path.exists(path_output) or recover:
            meteva.base.tool.path_tools.creat_path(path_output)
            if grid is None:
                grd = meteva.base.io.read_gridwind_from_gds_file(path_input)
            else:
                grd = meteva.base.io.read_gridwind_from_gds_file(path_input,grid=grid)
            if grd is not None:
                meteva.base.io.write_griddata_to_nc(grd,path_output,effectiveNum)
                end = time.time()
                copyed_num +=1
                left_minutes = int((end - start) * ( file_num - i -1) / (copyed_num * 60)) + 1
                print("剩余" + str(left_minutes) + "分钟")
                print(path_output)



def copy_wind_gds_to_m11(input_root_dir,output_root_dir,effectiveNum = 3,recover= False,grid = None):
    input_root_dir = input_root_dir.replace("\\","/")
    output_root_dir = output_root_dir.replace("\\","/")
    if input_root_dir[-1] != "/":
        input_root_dir += "/"
    if output_root_dir[-1] != '/':
        output_root_dir += "/"
    (gds_dir,file_model) = os.path.split(input_root_dir)
    save_dir = output_root_dir
    file_list = meteva.base.tool.path_tools.get_path_list_in_dir(gds_dir)
    len_input = len(input_root_dir)
    file_num = len(file_list)
    start = time.time()
    copyed_num = 0
    for i in range(file_num):
        file = file_list[i]
        path_input = file.replace("\\","/")
        path_file = path_input[len_input:]
        path_output = output_root_dir + path_file
        if not os.path.exists(path_output) or recover:
            meteva.base.tool.path_tools.creat_path(path_output)
            if grid is None:
                grd = meteva.base.io.read_griddata_wind_from_gds_file(path_input)
            else:
                grd = meteva.base.io.read_gridwind_from_gds_file(path_input,grid=grid)
            if grd is not None:
                meteva.base.io.write_griddata_to_micaps11(grd,path_output,effectiveNum)
                end = time.time()
                copyed_num +=1
                left_minutes = int((end - start) * ( file_num - i -1) / (copyed_num * 60)) + 1
                print("剩余" + str(left_minutes) + "分钟")
                print(path_output)



def copy_wind_m2_to_m11(input_root_dir,output_root_dir,effectiveNum = 3,recover= False,grid = None):
    input_root_dir = input_root_dir.replace("\\","/")
    output_root_dir = output_root_dir.replace("\\","/")
    if input_root_dir[-1] != "/":
        input_root_dir += "/"
    if output_root_dir[-1] != '/':
        output_root_dir += "/"
    (gds_dir,file_model) = os.path.split(input_root_dir)
    save_dir = output_root_dir
    file_list = meteva.base.tool.path_tools.get_path_list_in_dir(gds_dir)
    len_input = len(input_root_dir)
    file_num = len(file_list)
    start = time.time()
    copyed_num = 0
    for i in range(file_num):
        file = file_list[i]
        path_input = file.replace("\\","/")
        path_file = path_input[len_input:]
        path_output = output_root_dir + path_file
        if not os.path.exists(path_output) or recover:
            meteva.base.tool.path_tools.creat_path(path_output)
            if grid is None:
                grd = meteva.base.io.read_griddata_wind_from_micaps2(path_input)
            else:
                grd = meteva.base.io.read_griddata_wind_from_micaps2(path_input,grid=grid)
            if grd is not None:
                meteva.base.io.write_griddata_to_micaps11(grd,path_output,effectiveNum)
                end = time.time()
                copyed_num +=1

                left_minutes = int((end - start) * ( file_num - i -1) / (copyed_num * 60)) + 1
                print("剩余" + str(left_minutes) + "分钟")
                print(path_output)



def copy_wind_m11_to_nc(input_root_dir,output_root_dir,effectiveNum = 3,recover= False,grid = None):
    input_root_dir = input_root_dir.replace("\\","/")
    output_root_dir = output_root_dir.replace("\\","/")
    if input_root_dir[-1] != "/":
        input_root_dir += "/"
    if output_root_dir[-1] != '/':
        output_root_dir += "/"
    (gds_dir,file_model) = os.path.split(input_root_dir)
    save_dir = output_root_dir
    file_list = meteva.base.tool.path_tools.get_path_list_in_dir(gds_dir)
    len_input = len(input_root_dir)
    file_num = len(file_list)
    start = time.time()
    copyed_num = 0
    for i in range(file_num):
        file = file_list[i]
        path_input = file.replace("\\","/")
        path_file = path_input[len_input:]
        path_output = output_root_dir + path_file+".nc"
        if not os.path.exists(path_output) or recover:
            meteva.base.tool.path_tools.creat_path(path_output)
            if grid is None:
                grd = meteva.base.io.read_griddata_wind_from_micap11(path_input)
            else:
                grd = meteva.base.io.read_gridwind_from_micap11(path_input,grid=grid)
            if grd is not None:
                meteva.base.io.write_griddata_to_nc(grd,path_output,effectiveNum)
                end = time.time()
                copyed_num +=1
                left_minutes = int((end - start) * ( file_num - i -1) / (copyed_num * 60))
                print("剩余" + str(left_minutes) + "分钟")
                print(path_output)


def download_gds_files_to_local(ip, port, gds_dir, local_dir,recover= False):
    print(gds_dir)
    filelist = meteva.base.tool.path_tools.get_gds_file_list_in_one_dir(ip, port, gds_dir)
    for file in filelist:
        save_path = local_dir +  "/" + file
        if not os.path.exists(save_path) or recover:
            service = GDSDataService(ip, port)
            if service is not None:
                status, response = service.getData(gds_dir, file)
                if status == 200:
                    ByteArrayResult = DataBlock_pb2.ByteArrayResult()
                    ByteArrayResult.ParseFromString(response)
                    meteva.base.tool.path_tools.creat_path(save_path)
                    br = open(save_path, 'wb')
                    br.write(ByteArrayResult.byteArray)
                    br.close()