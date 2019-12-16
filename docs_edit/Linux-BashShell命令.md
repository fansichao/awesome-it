# Linux-BashShell

tags: Linux Bash Shell Script 2019 年 12 月

## BashShell 简介

bash shell 是一个命令解释器，它在操作系统的最外层，负责用户程序与内核进行交互操作的一种接口，将用户输入的命令翻译给操作系统，并将处理后的结果输出至屏幕。

**bash shell 的作用** 使用 shell 实现对 Linux 系统的大部分管理，例如：文件管理、用户管理、权限管理、磁盘管理、网络管理、软件管理、应用管理……

## BashShell 使用

### 语法

### 功能模块

### Tips

#### 检查文件是否存在

```bash
if [ ! -d ${config_path} ]; then
    echo ">>> 配置文件${config_path}不存在"
    exit 0
fi

#shell判断文件夹是否存在
if [ ! -d "/Top" ]; then
 mkdir -p /Topfi

#shell判断文件,目录是否存在或者具有权限
folder="/Top"
file="/Top/test.txt"

# -x 参数判断 $folder 是否存在并且是否具有可执行权限
if [ ! -x "$folder"]; then
 mkdir "$folder"
fi

# -d 参数判断 $folder 是否存在
if [ ! -d "$folder"]; then
 mkdir "$folder"
fi

# -f 参数判断 $file 是否存在
if [ ! -f "$file" ]; then
 touch "$file"
fi

# -n 判断一个"变量"是否有值
if [ ! -n "$file" ]; then
 echo "$file 变量为空！"
 exit 0
fi

# 判断两个变量的字符串内容是否相同
if [ "$file1" = "$file2" ]; then
 echo "$file1 equal $file2"
else
 echo "$file1 not equal $file2"
fi
```

#### 检查字符串是否存在文件中

```bash
if cat ${bash_path} | grep "source ${out_path}" > /dev/null 2>&1
then
    # echo "source ${out_path} 已经存在"
    continue
else
    echo "source ${out_path}" >> ${bash_path}
fi
```

#### 读取配置文件 config.ini

配置文件`config.ini`

```bash
[CONFIG_NAME]
KEY1 = val1
KEY2 = val2
[CONFIG_NAME2]
KEY3 = val3
```

配置脚本 `build_env.sh` 内容，只能 `. build_env.sh`执行,否则需要手动`su - xxx`使环境变量生效

```bash
(env) [scfan@fdm ~]$ cat build_env.sh
#!/bin/bash
# >>>>>>>>>>>>>>>>>>>>> 项目配置 <<<<<<<<<<<<<<<<<<<<<<<<<<<<
# 功能说明
#   - 项目配置虚拟环境变量
#   - 参数检查-在项目代码中检查
#   - 支持参数清理,支持多次运行

# >>>>>>>>>>>>>>>>>>>>> 参数配置 <<<<<<<<<<<<<<<<<<<<<<<<<<<<
# 可修改
config_path=config.ini
out_path=~/.fdm_profile
# 不可修改
bash_path=~/.bash_profile

if [ ! -f ${config_path} ]; then
    echo ">>> 配置文件${config_path}不存在"
    exit 0
fi
# >>>>>>>>>>>>>>>>>>>>>  读取配置文件 <<<<<<<<<<<<<<<<<<<<<<<<<<<<
# 读取配置文件 所有信息

# 删除空白行
# 删除左右空格      `echo $name | awk '$1=$1'`
# 检查是否包含字符  [[ $name =~ "[" ]]
function read_config(){
    # 读取配置文件
    IFS="="
    while read -r name value
    do
        if [ "$name" != "" ] && [ "$value" == "" ] && [[ $name =~ "[" ]] && [[ $name =~ "]" ]]; then
            echo "# item $name" >> ${out_path}
        elif [ "$name" != "" ] && [ "$value" != "" ]; then
            # 去除左右空格
            name=`echo $name | awk '$1=$1'`
            value=`echo $value | awk '$1=$1'`
            echo "export ${name}=${value}"  >> ${out_path}
        else
            tmp=0
        fi
    done < ${config_path}
}

# >>> 读取配置文件-方式2-仅供参考
# __readINI [配置文件路径+名称] [节点名] [键值]
# function __readINI() {
#     INIFILE=$1; SECTION=$2; ITEM=$3
#     _readIni=`awk -F '=' '/['$SECTION']/{a=1}a==1&&$1~/'$ITEM'/{print $2;exit}' $INIFILE`
#     echo ${_readIni}
# }
# _IP=( $( __readINI $config_path Project_Name PROJECT_NAME ) )
# echo ${_IP} >> ${out_path}


function set_config(){
    # 使配置文件生效
    if cat ${bash_path} | grep "source ${out_path}" > /dev/null 2>&1
    then
        # echo "source ${out_path} 已经存在"
        tmp=0
    else
        echo "source ${out_path}" >> ${bash_path}
    fi

    . ${bash_path}
}

function clean_config(){
    # 清理配置
    echo "" > ${out_path}
}


clean_config;
read_config;
set_config;

```

脚本输出结果

```bash
# item [CONFIG_NAME]
export KEY1=val1
export KEY2=val2
# item [CONFIG_NAME2]
export KEY3=val3
```
