# Missing course

> 以下为本人参加学习 MIT-Missing-Semester 课程的笔记记录，若有疏漏错误，望友好指正！
>
> 课程网站链接 [Eng](https://missing.csail.mit.edu/2020/)
> 课程网站链接 [CH](https://missing-semester-cn.github.io/)
>
> 课程 [youtube视频](https://www.youtube.com/playlist?list=PLyzOVJj3bHQuloKGG59rS43e29ro7I57J)
>
> 课程中文字幕视频：
>
> - [Missing_Semi_中译组 (ch01— ch04)](https://space.bilibili.com/1010983811?spm_id_from=333.337.search-card.all.click)
> - [刘黑黑a (已完结，全11讲)](https://space.bilibili.com/518734451?spm_id_from=333.337.search-card.all.click)
>
> 特别感谢由 [CS自学指南](https://csdiy.wiki/) 提供的资源导航网站与各类解答，非常感谢！

virtual machine

username: Z1

password: z

[TOC]

## Shell

### 1. Types

- bash — Bourne Again Shell
  - open terminal: **ctrl+alt+t**
- Fish
- zsh
- powershell — windows

`win / Linux — Terminal`



### 2. Command

#### Environment Variable

shell 会根据命令 (`e.g. echo, date...`) 遍历环境变量里的所有目录，直到找到该程序



#### Root

root (Linux) ≈ administrator (windows)

`sudo` or `do as su`: su — super user



#### Bash

manner help: https://catonmat.net/archive?q=bash
						 https://catonmat.net/bash-one-liners-explained-part-one
						 https://catonmat.net/bash-one-liners-explained-part-two
						 https://catonmat.net/bash-one-liners-explained-part-three
						 https://catonmat.net/bash-one-liners-explained-part-four
						 https://catonmat.net/bash-one-liners-explained-part-five

##### command

1. echo

   ```bash
   echo > file
   # end up with ctrl + D / c (x try)
   ```

2. which

3. `pwd`: print working directory

4. `cd`: change directory

   - `.`: current dir

   - `..`: parent dir

5. `ls`

   ```bash
   ls -R
   # 递归列出目录结构
   
   ls -l
   # print more info
   drwxr-xr-x   2 root root  4096 9月  26 15:09 bin
   |[-][-][-]-   [---] [---]
   | |  |  | |     |     |
   | |  |  | |     |     +----------> 7. Group
   | |  |  | |     +----------------> 6. Owner
   | |  |  | +----------------------> 5. Alternate Access Method
   | |  |  +------------------------> 4. Others Permissions
   | |  +---------------------------> 3. Group Permissions
   | +------------------------------> 2. Owner Permissions
   +--------------------------------> 1. File Type
   
   
   # file type
   -: a regular file
   d: directory
   l: a symbolic link
   ... or any other special type of file
   
   see more at num 25 `chmod`
   ```

6. `flag`: default - no args

7. `option`: with args

8. `mv`: 2 args — [old_path    new_path]

   ​		rename in current dir / move it to a new dir

9. `cp`: 2 args — [source_path   path]

10. `rm`: remove a file (default: not recursive) ——  × rm a dir

11. `rmdir`: 只允许移除空目录

12. `mkdir`

13. `man`: manual pages
    [Michael Kerrisk - man7.org](https://www.man7.org/index.html)

14. `ctrl + L`: clear and go back to the top

15. `< file`: 重定向该程序的输入流为该文件的内容

    `> file`：重定向上述程序的输出流到该文件内

16. `cat`: print content of a file

17. `>>`: **append** (not overwrite)

18. `|`: 将左侧程序的输出作为右侧程序的输入

19. `tail -n`: 打印输出的最后n行
    `ls -l /| tail -n1 > ls.txt`
    
20. `curl --head --slient baidu.com`
    `curl --head --slient baidu.com | grep --ignore-case`
    `curl --head --slient baidu.com | grep -i content-length | cut --delimiter=' ' -f2`
    
21. `sudo`

22. `sysfs`: `cd /sys`

23. `sudo su`: run the following command as root

24. `tee`: take its input and write it to a file but also to standard out

25. `chmod`— [Chmod Command in Linux (File Permissions) | Linuxize](https://linuxize.com/post/chmod-command-in-linux/)

26. `wc`: word count
    `cat script.md | wc -l`: count lines of script.md totally `[-l: count lines]`

    ```bash
    `chmod [OPTIONS] [ugoa…][-+=]perms…[,…] FILE...`
    
    # perm: permissions
    r - 4 - read
    w - 2 - write: rename, create, delete
    x - 1 - excute: search — are u allowed to enter this dir
      - 0 - no permissions
    
    # [ugoa…]: user classes
    u - The file owner.
    g - The users who are members of the group.
    o - All other users.
    a - All users, identical to ugo.
    
    # [-+=]
    - - Removes the specified permissions.
    + - Adds specified permissions.
    = - Changes the current permissions to the specified permissions. 
    	If no permissions are specified after the = symbol, all permissions from the specified user class are removed.
    	
    `chmod [OPTIONS] NUMBER FILE...`
    # number: 0 - 7
    3 digits: FileOwner GroupUsers AllOthers
    # Give the file’s owner read, write and execute permissions
    # read and execute permissions to group members
    # no permissions to all other users
    chmod 750 dirname
    ```




##### Test example


```bash
echo $PATH
/usr/lib/jvm/jdk1.8.0_162/bin:/home/hadoop/bin:/home/hadoop/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/usr/local/hadoop/bin:/usr/local/hadoop/sbin

# 找到echo的程序目录
which echo
/bin/echo

cd /
# 返回根目录

cd ~
# 指向用户目录，即home

cd -
# -: dash
# 跳转到上次所处的目录

cd ./usr
go to usr dir under the current dir

ls -l
总用量 100
drwxr-xr-x   2 root root  4096 9月  26 15:09 bin
lrwxrwxrwx   1 root root    34 10月  9 10:58 initrd.img -> boot/initrd.img-4.15.0-142-generic
... ...

man ls
# maunal pages for 'ls'
# 'q' to quit

z@Master:~$ cd /sys
z@Master:/sys$ ls
block  bus  class  dev  devices  firmware  fs  hypervisor  kernel  module  power
# kernel parameters
# kernel: core of somputer

sudo echo 500 > brightness
# not allowed
# pipe and redirection 都是shell设定好的
# 因此该语句是告诉shell以参数echo 500运行sudo, 然后发送输出到brightness文件，但shell打开brightness时并没有用sudo

# echo 1 > /sys/net/ipv4_forward
↑ # 代表以root权限执行后续语句
z@Master:~$
		  ↑ $ 不是root
		  


z@Master:/$ sudo su
root@Master:/# 
root@Master:/# exit
exit

`echo 1060 | sudo tee brightness`: take `echo`'s output — 1060 as `tee`'s input
	`sudo tee brightness`: run tee as root
	
	
xdg-open --whole_filename--
# open it in the appropriate program
# e.g. xdg-open example.html
# 		it will open browser and then open the file
```



#### Powershell

- dir — ls

  ```powershell
  echo $Env:Path
  ```

  

- **path**: 描述计算机文件的位置
  	win: ‘\’ — slash
    			linux/mac: ‘/’ — backslash

- **absolute path**: full path to a file
       all begin with `\`
   **relative path**

- **stream**: input~ & output~

   ```bash
   < file: 重定向该程序的输入流为该文件的内容
   > file：重定向上述程序的输出流到该文件内
   
   cat: print content of a file
   ```

   

### 3. script

1. `foo`: assign variables
   		  access the value of the variable with `$foo`

   ```bash
   foo=bar
   # not foo = bar
   # the foo program with the 1st argument `=` and the 2nd arhument `bar`
   
   # difference: "" and ''
   foo=bar
   echo "$foo"
   # prints bar
   echo '$foo'
   # prints $foo
   ###############test###############
   z@Slave1:~$ echo "foo is $foo"
   foo is bar
   z@Slave1:~$ echo 'foo is $foo'
   foo is $foo
   ```

2. **control flow techniques**

   ```bash
   vim mcd.sh
   source mcd.sh
   mcd test
   
   mcd () {
       mkdir -p "$1" 	# create a dir
       cd "$1"			# move into it
   }
   ```

   ==**KEY WORDS**==

   - `$0` - Name of the script 脚本名称

   - `$1` to `$9` - Arguments to the script. `$1` is the 1st argument … .

   - `$@` - All the arguments (like `$1, $2, ...`)

   - `$#` - Number of arguments 

   - `$?` - Return code of the previous command 上一命令的返回码

     ```bash
     return 0(true) / 1(false)
     # `grep`: search string 'foobar' in mcd.sh
     grep foobar mcd.sh
     	1
     grep mkdir mcd.sh
         mkdir -p "$1"
     echo $?
     	0
     ```

   - `$$` - Process identification number (PID) for the current script

   - `!!` - Entire last command, including arguments. 获取完整的上一命令
              A common pattern is to execute a command only for it to fail due to missing permissions; you can quickly re-execute the command with sudo by doing `sudo !!`

     ```bash
     mkdir mis
     sudo !! # sudo mkdir mis
     #################example####################
     cd ..
     z@Slave1:~/Documents/mis$ !!
     cd ..
     ```

     

   - `$_` - Last argument from the last command. 上条命令的最后一个参数
              If you are in an interactive shell, you can also quickly get this value by typing `Esc` followed by `.` or `Alt+.`

     ```bash
     mkdir test
     cd $_
     # go into the dir test
     ```

     ​     

3. `-ne`: not equal

      ```bash
      #!/bin/bash shell识别需要用bash运行该程序
      
      echo "Starting program at $(date)" # Date will be substituted
      
      echo "Running program $0 with $# arguments with pid $$"
      
      for file in "$@"; do
          grep foobar "$file" > /dev/null 2> /dev/null
          # When pattern is not found, grep has exit status 1
          # We redirect STDOUT and STDERR to a null register since we do not care about them
          if [[ $? -ne 0 ]]; then
              echo "File $file does not have any foobar, adding one"
              echo "# foobar" >> "$file"
          fi
      done
      ```

      

4. `<( CMD )`: will execute CMD and place the output in a temporary file

      ```bash
      # current list
      ls
      Desktop    Downloads         Music     Public     Videos
      Documents  examples.desktop  Pictures  Templates
      
      # 
      cat <(ls) <(ls ..)
      Desktop
      Documents
      Downloads
      examples.desktop
      Music
      Pictures
      Public
      Templates
      Videos
      hadoop
      z
      
      # parent list
      cd ..
      ls
      hadoop  z
      ```

5. regular expression

      - `*.sh`
      - `project?`

      

6. `convert`

      ```bash
      convert image.png image.jpg
      convert image.{png,jpg}
      ```

      

7. `{sth,sth,...}`

      ```bash
      cp /path/to/project/{foo,bar,baz}.sh /newpath
      # Will expand to
      cp /path/to/project/foo.sh /path/to/project/bar.sh /path/to/project/baz.sh /newpath
      
      # Globbing techniques can also be combined
      mv *{.py,.sh} folder
      # Will move all *.py and *.sh files
      ```

      

8. `touch`

      ```bash
      mkdir foo bar
      # This creates files foo/a, foo/b, ... foo/h, bar/a, bar/b, ... bar/h
      touch {foo,bar}/{a..h}
      # be attention to the dot, '..' !!! just 2 dots!!!
      touch foo/x bar/y
      # Show differences between files in foo and bar
      diff <(ls foo) <(ls bar)
      # Outputs
      # < x
      # ---
      # > y
      ```

      

9. python

      `shebang`: execute this script with a python interpreter instead of a shell command

      ```python
      #!/usr/local/bin/python	该行称为 shebang 行
      #!/usr/bin/env python	使用了 `env` 的 shebang 行
      #						`env` 会利用 `PATH` 环境变量来进行定位
      
      import sys
      for arg in reversed(sys.argv[1:]):
          print(arg)短路运算法则
      ```

      

10. 短路运算法则

      `||`: or
      `&&`: and
      `;`: always run both sides

      ```bash
        false || echo "Oops, fail"
        # Oops, fail
        # run 'false', if false, then run echo.
        
        true || echo "Will not be printed"
        # trur, so it won't print anything
        
        true && echo "Things went well"
        # Things went well
        
        false && echo "Will not be printed"
        #
        
        true ; echo "This will always run"
        # This will always run
        
        false ; echo "This will always run"
        # This will alwaysrun**functions**
      ```

    ​    

11. run script
          脚本不能直接用脚本的名称运行，若当前位置在脚本的所在文件夹，那么就无法cd shell当前路径



###  4. Tools

`install cmd: sudo apt install name_of_tools` 

1. `tldr`

2. `convert`

3. `shellcheck`

   ```bash
   shellcheck mcd.sh
   ```

4. ##### Find files

   - `find`

     ```bash
     # .: for the current dir
     # Find all directories named src
     find . -name src -type d
     
     # Find all python files that have a folder named test in their path
     find . -path '*/test/*.py' -type f
     
     # Find all files modified in the last day
     find . -mtime -1
     
     # Find all zip files with size in range 500k to 10M
     find . -size +500k -size -10M -name '*.tar.gz'
     
     # Delete all files with .tmp extension
     find . -name '*.tmp' -exec rm {} \;
     
     # Find all PNG files and convert them to JPG
     find . -name '*.png' -exec convert {} {}.jpg \;
     ```

   - `fdfind`: Ubuntu 系统下避免命名冲突，`fd` → `fdfind`

   - `locate`: compiling some sort of index or database for quickly searching

   ​				updated using `updatedb`

5. ##### Find codes

   - `grep`

   - `rg`

     ```bash
     # -t py: only find python files
     # Find all python files where I used the requests library
     rg -t py 'import requests'
     
     # -u: including hidden files
     # Find all files without a shebang line
     rg -u --files-without-match "^#\!"
     
     # Find all matches of foo and print the following 5 lines
     rg foo -A 5
     
     # 查找结果上下的5行
     rg foo -C 5
     
     # Print statistics of matches (# of matched lines and files )
     rg --stats PATTERN
     ```

   - `ripgrep`

   - `ack`

   - `ag`

6. ##### Finding shell commands

   - UP/DOWN arrows

   - `history`

     ```bash
     history
     
     history 1
     
     history 1 | grep convert
     
     # ctrl + r: backward search
     ```

     go to the [appendix](# 1. cmd history)

   - `fzf`: fuzzy finder (interactive `grep`)

7. ##### Directory Navigation

   - `ls`

     ```bash
     ls -R
     # list out structure of dir recursively
     ```

   - `tree`

   - `broot`

     - fuzzy maps
     - select / choose

   - `nnn`: interactive surface

   - `autojump`



## Vim

### fundamental

based on **Modal**



### Modal

1. **Normal**: for moving around a file and making edits (browse and edit)
   `i` — Insert
   `R / shift + r` — replace
   `v` —visual
   `shift + v` —visual line
   `ctrl + v` — visual block
   `esc` — Normal
   `:` — command line
2. **Insert**: for inserting text
3. **replace**: for replacing text
4. **selector**: for selecting blocks of text
   visual, visual line, visual block
5. **command line**: for running a command



### Basics

#### cmd

1. `:q` quit (close window)
2. `:w` save (“write”)
3. `:wq` save and quit
4. `:e {name of file}` open file for editing
5. `:ls` show open buffers
6. `:help {topic}` open help
   - `:help :w` opens help for the `:w` command
   - `:help w` opens help for the `w` movement

#### Movement — Normal mode

- Basic movement: `hjkl` (left, down, up, right)

- Words: `w` (next word), `b` (beginning of word), `e` (end of word)

- Lines: `0` (beginning of line), `^` (first non-blank character), `$` (end of line)

- Screen: `H` (top of screen), `M` (middle of screen), `L` (bottom of screen)

- Scroll: `Ctrl-u` (up), `Ctrl-d` (down)

- File: `gg` (beginning of file), `G` (end of file)

- Line numbers: `:{number}<CR>` or `{number}G` (line {number})

- Misc: `%` (corresponding item)

- Find:

   `f{character}`: find {character} forward

  `t{character}`: to {character} forward

   `F{character}`: find {character} backward

  `T{character}`: to {character} backward

  - `,` / `;` for navigating matches

- Search: `/{regex}`, `n` / `N` for navigating matches



#### Selection — Visual mode

- Visual: `v`
- Visual Line: `V`
- Visual Block: `Ctrl-v`

Can use movement keys to make selection.



#### Edits

Everything that you used to do with the mouse, you now do with the keyboard using editing commands that compose with movement commands. Here’s where Vim’s interface starts to look like a programming language. Vim’s editing commands are also called “verbs”, because verbs act on nouns.

- `i`: enter Insert mode
  - but for manipulating/deleting text, want to use something more than backspace
- `o` / `O` insert line below / above
  open a new line and enter the Insert mode
- `d{motion}`: delete {motion}
  - `dw` is delete word
    `d$` is delete to end of line
    `d0` is delete to beginning of line
- `c{motion}`: change {motion}
  - `cw` is change word
  - like `d{motion}` followed by `i`
- `x` delete character (equal do `dl`)
- `s` substitute character (equal to `cl`)
- Visual mode + manipulation
  - select text, `d` to delete it or `c` to change it
- `u` to undo, `<C-r>` to redo
- `y` to copy / “yank” (some other commands like `d` also copy)
- `p` to paste
- Lots more to learn: e.g. `~` flips the case of a character



#### Counts

You can combine nouns and verbs with a count, which will perform a given action a number of times.

- `3w` move 3 words forward

- `5j` move 5 lines down

- `7dw` delete 7 words

  

#### Modifiers

You can use modifiers to change the meaning of a noun. Some modifiers are `i`, which means “inner” or “inside”, and `a`, which means “around”.

- `ci(` change the contents inside the current pair of parentheses
- `ci[` change the contents inside the current pair of square brackets
- `da'` delete a single-quoted string, including the surrounding single quotes





## Data Wrangling

### Introduction

load server’s log

```bash
ssh myserver journalctl
```

load lines with `sshd`

```bash
ssh myserver journalctl | grep sshd
```

Notice that we’re using a pipe to stream a *remote* file through `grep` on our local computer! `ssh` is magical, and we will talk more about it in the next lecture on the command-line environment. This is still way more stuff than we wanted though. And pretty hard to read. Let’s do better:

```bash
ssh myserver 'journalctl | grep sshd | grep "Disconnected from"' | less
```

quoting: filtering on the remote server, and then massage the data locally.

`less` gives us a “pager” that allows us to scroll up and down through the long output. To save some additional traffic while we debug our command-line, we can even stick the current filtered logs into a file so that we don’t have to access the network while developing:

```bash
$ ssh myserver 'journalctl | grep sshd | grep "Disconnected from"' > ssh.log
$ less ssh.log
```

There’s still a lot of noise here. There are *a lot* of ways to get rid of that, but let’s look at one of the most powerful tools in your toolkit: `sed`.



### Tools

#### sed

[top](# Missing course)

a “stream editor”: give short commands for how to modify the file, rather than manipulate its contents directly.

`s`: substitution

> ++++++++++++++++++++++++++ see here for Full commands ++++++++++++++++++++++++++

```bash
ssh myserver journalctl
 | grep sshd
 | grep "Disconnected from"
 | sed -E 's/.*Disconnected from (invalid |authenticating )?user (.*) [^ ]+ port [0-9]+( \[preauth\])?$/\2/'
 | sort | uniq -c
 | sort -nk1,1 | tail -n10
 | awk '{print $2}' | paste -sd,
```

use a simple ***regular expression***

- a powerful construct that lets you match text against pattern
- The `s` command is written on the form: `s/REGEX/SUBSTITUTION/`
  `REGEX`: the regular expression you want to search for
  `SUBSTITUTION`: the text you want to substitute matching text with

##### usage

```bash
sed -E 's/REGEX/SUBSTITUTION/'
# -E: allows u to match some sign ignoring its surface meaning
```

**sth of `capture groups` — regular expression**

Any text matched by a regex surrounded by parentheses `()` is stored in a numbered capture group. 
`I want to remember this value and reuse it later`

```bash
 | sed -E 's/.*Disconnected from (invalid |authenticating )?user (.*) [^ ]+ port [0-9]+( \[preauth\])?$/\2/'
 # in this case, (invalid |authenticating ) ---> 1st group ---> \1
 #				 (.*) 						---> 2nd group ---> \2
```



#### sort

```bash
# input: lots of lines —> sorts —> output
| sort

# -n: numeric sort
# -k: let select a whitespace-separated column from the input to sort by
| sort -nk1,1
```



#### uniq

only print unique lines

```bash
# -c: collapse consecutive lines that are the same into a single line, prefixed with a count of the number of occurrences.
| uniq -c
```



#### tail

```bash
# -n(number): select the last 20 lines
| tail -n20
```





### CtrlP

#### Installation

```bash
mkdir -p ~/.vim/pack/plugins/start
git clone --depth=1 https://github.com/ctrlpvim/ctrlp.vim.git ~/.vim/pack/plugins/start/ctrlp
```



#### usage

##### a. Start

​	`^P` / `:CtrlP` under vim terminal mode

##### b. Mode

1. `:CtrlP` or `:CtrlP [starting-directory]`
   invoke CtrlP
2. `:CtrlPBuffer`
   find buffer
3. `:CtrlPMRU`
   find MRU file mode.
4. `:CtrlPMixed`
   search in Files, Buffers and MRU files at the same time

##### c. quick mode

1. `^D`
   search by files `names` or `path`

2. `^F` / `^B`
   search — `buffers` opened files
   			 — `mru files` recent files
   			 — `files` files under current directory

   command line shows `<mru>={ files }=<buf>` —— `{}` shows the current mode

3. `^R`
   open regular expression match mode





## Command-line Environment

```python
#!/usr/bin/env python
from __future__ import print_function
import signal, time

def handler(signum, time):
    print("\nI got a SIGINT, but I am not stopping")

signal.signal(signal.SIGINT, handler)
i = 0
# while True:
for i in range(100):
    time.sleep(.1)
    print("\r{}".format(i), end="")
    i += 1
```



### signal

```bash
# sleep 10 seconds
sleep 10
^C
```

`man signal`

1. `SIGINT ---- ^C`
   signal interrupt
   interrupt program ---- to stop itself
2. `SIGQUIT ---- ^\`
   quit program
3. `SIGTERM`
   `kill -TERM <PID>`
4. `SIGSTOP`: stop process
   `SIGCONT`: continue after stop
5. `SIGTSTP ---- ^Z`
   `TSTP`: Terminal Stop



### processes commands

1. `bg`
   continue running a stopped process in the **background**
2. `fg`
   continue running a stopped process and recover it to **foreground**
3. `nohup`
   ignoring input and appending output to 'nohup.out'
4. `jobs`
   lists the unfinished jobs associated with the current terminal session
5. `kill`
6. `&`
   run the command in the background
7. `$!`
   select the recent files

```bash
sleep 1000
^Z
[1]+  Stopped                 sleep 1000

# &: start this process running in the background
# nohup: ignore any kind of hang up signal (挂断信号) and keep running
nohup sleep 200 &
# OUTPUT
[2] 18745
appending output to nohup.out

# show all jobs started -- running, suspended, stopped
jobs
# OUTPUT
[1]  + suspended  sleep 1000
[2]  - running    nohup sleep 2000

# bg %num: continue running the [num] processes
# num: identifier of a process
bg %1
#output
[1]  - 18653 continued  sleep 1000

jobs
[1]  - running    sleep 1000
[2]  + running    nohup sleep 2000

# kill -STOP %num
# stop num program by sending a signal
kill -STOP %1
[1]  + 18653 suspended (signal)  sleep 1000sl
$ jobs
[1]  + suspended (signal)  sleep 1000
[2]  - running    nohup sleep 2000

# 1 can be hang up
kill -SIGHUP %1 # -SIGHUP -- -HUP
[1]  + 18653 hangup     sleep 1000
jobs
[2]  + running    nohup sleep 2000

# 2 can't be hang up
kill -SIGHUP %2
jobs
[2]  + running    nohup sleep 2000

# 2 can be killed
kill %2 # kill -KILL %num
[2]  + 18745 terminated  nohup sleep 2000
```







### Tmux

Terminal Multiplexers 终端多路复用 [同时执行多个任务]

- Sessions
  - Windows
    - Panes

#### Sessions

1. `tmux` is separated from `shell`

2. start

   ```
   tmux
   ```

3. detach

   - `tmux detach`
   - `^B + D` 

   both are right

4. enter a session
   `tmux a -t [session num]`

5. create a named session
   `tmux new -s foobar` — new session named by `foobar`

6. end
   `^D`

7. 



#### Windows

1. `^B` + `C`
   create a new window

2. `^B` + `D`
   close a window

3. `^B` + `P`
   change to previous one

   `^B` + `N`
   next one

4. `^B` + `[num]`
   change to `[num]` window

5. `^B` + `,`
   rename the current window

6. `^B` + `z`
   zoom into a window
   go back

7. 



#### Pane

1. `^B` + `“`
   display a session into 2 panes vertically
2. `^B` + `%`
   keep splitting panes horizontally
3. `^B` + direction keys
   change panes among panes
4. `^B` + space
   rearrange panes in many different layouts
5. `^B` + `[`
6. `exit`



https://blog.csdn.net/lell3538/article/details/82150733





### dotfiles

#### Alias

make long commands shorter

##### syntax

1. `alias ll="ls -lah"`
   no spaces like: `alias ll = "ls -lah"`
2. `alias ll`
   ask `alias` the actual command `ll='ls -lah'`
3. `alias dc=cd`
   `dc Documents`
   make `dc` same as `cd`
4. `PS1="> "`
   work on `zsh` to change `bash-5.0$` into `> `
   `PS1="\w > "`: `~/cmd > `

##### ways

1. temporary
   all `alias` in the **shell** only work in the current shell
2. permanent
   `~/.bashrc`



#### symlinks

control version
tidier and neater into a folder

##### syntax

```bash
ln -s path/to/file symlink
```





### remote machines

**SSH**: Secure Shell

#### connect

`foo`: username to connect in the remote machine
`@`: tell terminal that this separates what the user is from what the address is
`bar.mit.edu`: the remote machine `url` / `ip` (192.168.1.42)

```bash
ssh foo@bar.mit.edu
```



#### Executing commands

```bash
# grep locally the remote output of ls
ssh foobar@server ls | grep PATTERN

# grep remotely the local output of ls
ls | ssh foobar@server grep PATTERN
```



#### SSH Keys









## Practice

### CH01

1. For this course, you need to be using a Unix shell like Bash or ZSH. If you are on Linux or macOS, you don’t have to do anything special. If you are on Windows, you need to make sure you are not running cmd.exe or PowerShell; you can use [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/) or a Linux virtual machine to use Unix-style command-line tools. To make sure you’re running an appropriate shell, you can try the command `echo $SHELL`. If it says something like `/bin/bash` or `/usr/bin/zsh`, that means you’re running the right program.

2. Create a new directory called `missing` under `/tmp`.

3. Look up the `touch` program. The `man` program is your friend.

4. Use `touch` to create a new file called `semester` in `missing`.

5. Write the following into that file, one line at a time:

   ```bash
   #!/bin/sh
   curl --head --silent https://missing.csail.mit.edu
   ```

   The first line might be tricky to get working. It’s helpful to know that `#` starts a comment in Bash, and `!` has a special meaning even within double-quoted (`"`) strings. Bash treats single-quoted strings (`'`) differently: they will do the trick in this case. See the Bash [quoting](https://www.gnu.org/software/bash/manual/html_node/Quoting.html) manual page for more information.

6. Try to execute the file, i.e. type the path to the script (`./semester`) into your shell and press enter. Understand why it doesn’t work by consulting the output of `ls` (hint: look at the permission bits of the file).

7. Run the command by explicitly starting the `sh` interpreter, and giving it the file `semester` as the first argument, i.e. `sh semester`. Why does this work, while `./semester` didn’t?

8. Look up the `chmod` program (e.g. use `man chmod`).

9. Use `chmod` to make it possible to run the command `./semester` rather than having to type `sh semester`. How does your shell know that the file is supposed to be interpreted using `sh`? See this page on the [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)) line for more information.

10. Use `|` and `>` to write the “last modified” date output by `semester` into a file called `last-modified.txt` in your home directory.

11. Write a command that reads out your laptop battery’s power level or your desktop machine’s CPU temperature from `/sys`. Note: if you’re a macOS user, your OS doesn’t have sysfs, so you can skip this exercise.

```bash
# echo $SHELL
# /bin/bash
# man touch
# touch semester

# echo < semester
# not worked

# cat > semester
#!/bin/sh
curl --head --silent https://missing.csail.mimt.edu

# cat < semester
#!/bin/sh
curl --head --silent https://missing.csail.mimt.edu

# ./semester
bash: ./semester: Permission denied

# ls -l semester
total 24
-rw-rw-r-- 1 z z  62 10月 20 16:40 semester

# chmod 777 semester

# ls -l semester
total 24
-rwxrwxrwx 1 z z  62 10月 20 16:40 semester

# ./semester | grep Last-Modified > last_modified.log
# ls -l semester
total 28
-rwxrwxrwx 1 z z  61 10月 20 18:26 semester
# cat < last_modified.log
Last-Modified: Sat, 19 Oct 2024 09:20:59 GMT

#  > cat /sys/class/power_supply/BAT0/capacity
79
```



### CH02

1. Read `man ls` and write an `ls` command that lists files in the following manner

   - Includes all files, including hidden files
     `-a`

   - Sizes are listed in human readable format (e.g. 454M instead of 454279954)
     `-h`

   - Files are ordered by recency `最近访问顺序`
     `-t`

   - Output is colorized
     `--color`

     ```bash
     ls -a -h -t --color -l
     total 20K
     drwxrwxr-x 2 z z 4.0K 10月 18 18:59 .
     -rwxrwxr-x 1 z z   86 10月 18 18:59 ch02_02_script.py
     -rw-rw-r-- 1 z z   51 10月 18 18:36 mcd.sh
     -rwxrwxr-x 1 z z  333 10月 18 18:34 ch02_01_example.sh
     drwxr-xr-x 3 z z 4.0K 10月 17 11:34 ..
     ```

   

2. Write bash functions `marco` and `polo` that do the following.
   Whenever you execute `marco` the current working directory should be saved in some manner, then when you execute `polo`, no matter what directory you are in, `polo` should `cd` you back to the directory where you executed `marco`. For ease of debugging you can write the code in a file `marco.sh` and (re)load the definitions to your shell by executing `source marco.sh`.

   - 需要手动键入，否则报错`command not found`

   ```bash
   #!/bin/bash
   marco(){
   	echo "$(pwd)" > /home/z/Documents/mis/marco_history.log
   	echo "save pwd $(pwd)"
   }
   
   polo(){
   	cd "$(cat "/home/z/Documents/mis/marco_history.log")"
   }
   
   
    #!/bin/bash
    marco(){
        echo "$(pwd)" > $HOME/marco_history.log
        echo "save pwd $(pwd)"
    }
    polo(){
        cd "$(cat "$HOME/marco_history.log")"
    }
   ```

   

3. Say you have a command that fails rarely. In order to debug it you need to capture its output but it can be time consuming to get a failure run. Write a bash script that runs the following script until it fails and captures its standard output and error streams to files and prints everything at the end. Bonus points if you can also report how many runs it took for the script to fail.

   - `buggy.sh`

   ```bash
    #!/usr/bin/env bash
   
    n=$(( RANDOM % 100 ))
   
    if [[ n -eq 42 ]]; then
       echo "Something went wrong"
       >&2 echo "The error was using magic numbers"
       exit 1
    fi
   
    echo "Everything went according to plan"
   ```

   - `while` version

   ```bash
    #!/usr/bin/env bash
    
   cnt=0
   echo > output.log # redirect the last time output to output.log 
   while true
   do
   	./buggy.sh &>> output.log
   	# &>> redirect both stdout and stderr then append to output.log
   	# details see at https://catonmat.net/bash-one-liners-explained-part-three
   	if [[$? -ne 0]]; then
   		cat output.log
   		echo "failed after $cnt times"
   		break	# 跳出循环
   	fi
   	((cnt++))
   
   done
   ```

   - `for` version

   ```bash
    #!/usr/bin/env bash
    echo > out.log
    for ((count=0;;count++))
    do
        ./buggy.sh &>> out.log
        if [[ $? -ne 0 ]]; then
            echo "failed after $count times"
            break
   
        fi
    done
   ```

   

4. As we covered in the lecture `find`’s `-exec` can be very powerful for performing operations over the files we are searching for. However, what if we want to do something with **all** the files, like creating a zip file? As you have seen so far commands will take input from both arguments and STDIN. When piping commands, we are connecting STDOUT to STDIN, but some commands like `tar` take inputs from arguments. To bridge this disconnect there’s the [`xargs`](https://www.man7.org/linux/man-pages/man1/xargs.1.html) command which will execute a command using STDIN as arguments. For example `ls | xargs rm` will delete the files in the current directory.

   Your task is to write a command that recursively finds all HTML files in the folder and makes a zip with them. Note that your command should work even if the files have spaces (hint: check `-d` flag for `xargs`).

   ```bash
   find . -name '*.html' -type f convert {} {}.zip \ | xargs -d '\n'
   ```

    `xargs -d`: 输入以指定字符结尾
   					 e.g. `xargs -d '\n'` —— 指定输入仅由换行符分隔的项组成

   

5. (Advanced) Write a command or script to recursively find the most recently modified file in a directory. More generally, can you list all files by recency?

   ```bash
   find . -type f -print0 | xargs -0 ls -lt | head -1
   ```

   `ls -lt`: list out file by chronological order
   `xargs -0`: print out all file under sub-dirs
   `head -1`: return the latest file







### CH04

[top](# Missing course)

1. Take this [short interactive regex tutorial](https://regexone.com/).

2. Find the number of words (in `/usr/share/dict/words`) that contain at least three `a`s and don’t have a `'s` ending. What are the three most common last two letters of those words? `sed`’s `y` command, or the `tr` program, may help you with case insensitivity. How many of those two-letter combinations are there? And for a challenge: which combinations do not occur?

   统计包含3个a以上且不以‘s结尾的单词个数

   ```bash
   cat /usr/share/dict/words | tr "[:upper:]" "[:lower:]" | grep -E "^([^a]*a){3}.*$" | grep -v "'s$" | wc -l
   ```

   - `tr "[:upper:]" "[:lower:]"`: ignore case 忽略大小写
   - `grep -E "^([^a]*a){3}.*$" ` 包含3个a及以上的字符串
     - `-E`: **extended regular expressions** (ERE)
       	   allows more complex regex features, such as grouping with `()` and quantifiers like `{}`.
     - `^`: 从每行开头开始匹配
     - `[^a]*`：匹配零个或多个 **非 "a"** 的字符
       				`[^a]` 是一个**取反字符类**，排除了 "a
             				表示在每个 "a" 前可以有任意字符组合（或无字符），但不能包含 "a"。
     - `a`：在 `[^a]*` 的非 "a" 字符序列之后，匹配一个 "a" 字符
   - `grep -v "\'s$"`: 匹配 ‘s 结尾的字符串后取反
   - `wc -l`: 统计行数

   ```bash
   grep -i 'a.*a.*a' /usr/share/dict/words | grep -vi 's$' | sed 's/.*\(..\)$/\1/' | sort | uniq | wc -l
   ```

   - `grep -i`: ignore case

   

   

   

3. To do in-place substitution it is quite tempting to do something like `sed s/REGEX/SUBSTITUTION/ input.txt > input.txt`. However this is a bad idea, why? Is this particular to `sed`? Use `man sed` to find out how to accomplish this.

4. Find your average, median, and max system boot time over the last ten boots. Use `journalctl` on Linux and `log show`on macOS, and look for log timestamps near the beginning and end of each boot. On Linux, they may look something like:

   ```
   Logs begin at ...
   ```

   and

   ```
   systemd[577]: Startup finished in ...
   ```

   On macOS, [look for](https://eclecticlight.co/2018/03/21/macos-unified-log-3-finding-your-way/):

   ```
   === system boot:
   ```

   and

   ```
   Previous shutdown cause: 5
   ```

5. Look for boot messages that are *not* shared between your past three reboots (see `journalctl`’s `-b` flag). Break this task down into multiple steps. First, find a way to get just the logs from the past three boots. There may be an applicable flag on the tool you use to extract the boot logs, or you can use `sed '0,/STRING/d'` to remove all lines previous to one that matches `STRING`. Next, remove any parts of the line that *always* varies (like the timestamp). Then, de-duplicate the input lines and keep a count of each one (`uniq` is your friend). And finally, eliminate any line whose count is 3 (since it *was* shared among all the boots).

6. Find an online data set like [this one](https://stats.wikimedia.org/EN/TablesWikipediaZZ.htm), [this one](https://ucr.fbi.gov/crime-in-the-u.s/2016/crime-in-the-u.s.-2016/topic-pages/tables/table-1), or maybe one [from here](https://www.springboard.com/blog/data-science/free-public-data-sets-data-science-project/). Fetch it using `curl` and extract out just two columns of numerical data. If you’re fetching HTML data, [`pup`](https://github.com/EricChiang/pup) might be helpful. For JSON data, try [`jq`](https://stedolan.github.io/jq/). Find the min and max of one column in a single command, and the difference of the sum of each column in another.







### CH05

```bash
# create a process
sleep 10000
^Z
[1]+  Stopped                 sleep 10000

# continue process
bg
[1]+ sleep 10000 &

# get pid and full command line
pgrep -a sleep
5152 sleep 10000

# get pid by full process name
pgrep -f sleep
5152

# I dont know
pgrep -af sleep
5152 sleep 10000

jobs
[1]+  Stopped                 sleep 10000
bg
[1]+ sleep 10000 &
jobs
[1]+  Running                 sleep 10000 &

# kill process by full process name
pkill -f sleep
[1]+  Terminated              sleep 10000
```





## Appendix

### 1. `cmd history`

```bash
 history
    1  sudo apt-get install virtualbox-guest-dkms
    2  sudo useradd -m hadhoop -s /bin/bash
    3  sudo passwd hadoop
    4  sudo userdel -r hadoop
    5  sudo userdel -r hadhoop
    6  sudo userdel hadoop
    7  sudo userdel hadhoop
    8  clear
    9  sudo useradd -m hadoop -s /bin/bash
   10  sudo passwd hadoop
   11  sudo adduser hadoop sudo
   12  sudo apt-get install virtualbox-guest-dkms
   13  echo hello\ wo
   14  Slave1:~$ ^C
   15  z@Slave1:~$ ^C
   16  foo=bar
   17  echo $foo
   18  echo "foo is $foo"
   19  echo 'foo is $foo'
   20  echo $shell
   21  echo $SHELL
   22  ls
   23  exit
   24  ls
   25  cd documents
   26  cd Documents
   27  mkdir mis/ch02
   28  mkdir /mis/ch02
   29  mkdir /mis
   30  mkdir mis/
   31  ls
   32  mkdir mis/ch02
   33  ls
   34  cd mis
   35  ls
   36  cd ch02
   37  cd ..
   38  cd mis/ch02
   39  vim mcd.sh
   40  ls
   41  vim mcd.sh
   42  ls
   43  echo < mcd.sh
   44  echo $?
   45  grep foobar mcd.sh
   46  echo $?
   47  grep mkdir mcd.sh
   48  echo $?
   49  false ; echo "This will always run"
   50  foo=$(pwd)
   51  echo "$foo
   52  exit
   53  ls
   54  cat <(ls) <(ls ..)
   55  cd ..
   56  ls
   57  cd ..
   58  ls
   59  cd ~
   60  ls
   61  cd Documents
   62  ls
   63  cd mis/ch02
   64  ls
   65  vim ch02_01_example.sh
   66  ls
   67  vim ch02_01_example.sh
   68  ls
   69  ch02_01_example.sh mcd.sh ch02_01_example.sh
   70  ./ch02_01_example.sh mcd.sh ch02_01_example.sh
   71  vim mcd.sh
   72  cd ..
   73  ./ch02_02_script.py a b c
   74  shellsheck mcd.sh
   75  shellcheck mcd.sh
   76  cd ~
   77  find . -name "*.tmp"
   78  cd /
   79  find . -name "*.tmp"
   80  sudo find . -name "*.tmp"
   81  locate tmp
   82  cd ~/Documents/mis/
   83  ls
   84  grep foobar mcd.sh
   85  grep -R foobar .
   86  history
```



### 2. `env configuration`

```bash
z1@z1-VirtualBox:~$ sudo apt-get install openssh-server
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following additional packages will be installed:
  ncurses-term openssh-sftp-server ssh-import-id
Suggested packages:
  ssh-askpass rssh molly-guard monkeysphere
The following NEW packages will be installed:
  ncurses-term openssh-server openssh-sftp-server ssh-import-id
0 upgraded, 4 newly installed, 0 to remove and 192 not upgraded.
Need to get 633 kB of archives.
After this operation, 5,136 kB of additional disk space will be used.
Do you want to continue? [Y/n] y
Get:1 http://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial/main amd64 ncurses-term all 6.0+20160213-1ubuntu1 [249 kB]
Get:2 http://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial-updates/main amd64 openssh-sftp-server amd64 1:7.2p2-4ubuntu2.10 [38.8 kB]
Get:3 http://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial-updates/main amd64 openssh-server amd64 1:7.2p2-4ubuntu2.10 [335 kB]
Get:4 http://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial/main amd64 ssh-import-id all 5.5-0ubuntu1 [10.2 kB]
Fetched 633 kB in 4s (147 kB/s)     
Preconfiguring packages ...
Selecting previously unselected package ncurses-term.
(Reading database ... 178803 files and directories currently installed.)
Preparing to unpack .../ncurses-term_6.0+20160213-1ubuntu1_all.deb ...
Unpacking ncurses-term (6.0+20160213-1ubuntu1) ...
Selecting previously unselected package openssh-sftp-server.
Preparing to unpack .../openssh-sftp-server_1%3a7.2p2-4ubuntu2.10_amd64.deb ...
Unpacking openssh-sftp-server (1:7.2p2-4ubuntu2.10) ...
Selecting previously unselected package openssh-server.
Preparing to unpack .../openssh-server_1%3a7.2p2-4ubuntu2.10_amd64.deb ...
Unpacking openssh-server (1:7.2p2-4ubuntu2.10) ...
Selecting previously unselected package ssh-import-id.
Preparing to unpack .../ssh-import-id_5.5-0ubuntu1_all.deb ...
Unpacking ssh-import-id (5.5-0ubuntu1) ...
Processing triggers for man-db (2.7.5-1) ...
Processing triggers for ureadahead (0.100.0-19.1) ...
Processing triggers for systemd (229-4ubuntu21.28) ...
Processing triggers for ufw (0.35-0ubuntu2) ...
Setting up ncurses-term (6.0+20160213-1ubuntu1) ...
Setting up openssh-sftp-server (1:7.2p2-4ubuntu2.10) ...
Setting up openssh-server (1:7.2p2-4ubuntu2.10) ...
Creating SSH2 RSA key; this may take some time ...
2048 SHA256:prhhkMh3R/yadMGXiR4TTsGxRPQCQFBuqB6suq+MjTk root@z1-VirtualBox (RSA)
Creating SSH2 DSA key; this may take some time ...
1024 SHA256:tUzVSB0CCgxsHEa/U/1lIP67r93Qt9xG4WyBnuGOsfM root@z1-VirtualBox (DSA)
Creating SSH2 ECDSA key; this may take some time ...
256 SHA256:RX60oqGc1vOJJdiBtUrMEL2Q5zSy8nE12djcoEymqOw root@z1-VirtualBox (ECDSA)
Creating SSH2 ED25519 key; this may take some time ...
256 SHA256:eU1sOtb0HLEOwaAIBRPv/7Rx8ne4NOjEFJSgwY/2svI root@z1-VirtualBox (ED25519)
Setting up ssh-import-id (5.5-0ubuntu1) ...
Processing triggers for ureadahead (0.100.0-19.1) ...
Processing triggers for systemd (229-4ubuntu21.28) ...
Processing triggers for ufw (0.35-0ubuntu2) ...
z1@z1-VirtualBox:~$ ssh localhost
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:RX60oqGc1vOJJdiBtUrMEL2Q5zSy8nE12djcoEymqOw.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'localhost' (ECDSA) to the list of known hosts.
z1@localhost's password: 
Welcome to Ubuntu 16.04.7 LTS (GNU/Linux 4.15.0-112-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage


193 packages can be updated.
158 updates are security updates.

New release '18.04.6 LTS' available.
Run 'do-release-upgrade' to upgrade to it.


The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

z1@z1-VirtualBox:~$ exit
logout
Connection to localhost closed.
z1@z1-VirtualBox:~$ cd ~/.ssh/
z1@z1-VirtualBox:~/.ssh$ ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/home/z1/.ssh/id_rsa): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/z1/.ssh/id_rsa.
Your public key has been saved in /home/z1/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:akRisdSlKk4CpGDqarfrgufEKcz255UnOyGtRVGisEI z1@z1-VirtualBox
The key's randomart image is:
+---[RSA 2048]----+
|.E .o. oo.       |
|B  .oooo.        |
|+. .+.o .        |
|o .. + .         |
|..o . + S        |
|+= o o =.        |
|+==.  *+..       |
|+++ .+..+        |
| o+=+. ..        |
+----[SHA256]-----+
z1@z1-VirtualBox:~/.ssh$ cat ./id_rsa.pub >> ./authorized_keys
z1@z1-VirtualBox:~/.ssh$ ssh localhost
Welcome to Ubuntu 16.04.7 LTS (GNU/Linux 4.15.0-112-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage


193 packages can be updated.
158 updates are security updates.

New release '18.04.6 LTS' available.
Run 'do-release-upgrade' to upgrade to it.

Last login: Fri Nov  1 16:44:59 2024 from 127.0.0.1
z1@z1-VirtualBox:~$ exit
logout
Connection to localhost closed.


# ==================== IP ========================
z1@z1-VirtualBox:~/.ssh$ ifconfig
enp0s3    Link encap:Ethernet  HWaddr 08:00:27:02:93:03  
          inet addr:192.168.56.106  Bcast:192.168.56.255  Mask:255.255.255.0
          inet6 addr: fe80::c3e4:bfc6:156:98b2/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:5546 errors:0 dropped:0 overruns:0 frame:0
          TX packets:800 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:7736715 (7.7 MB)  TX bytes:68351 (68.3 KB)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:768 errors:0 dropped:0 overruns:0 frame:0
          TX packets:768 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:68791 (68.7 KB)  TX bytes:68791 (68.7 KB)
          
z1@z1-VirtualBox:~$ tmux
The program 'tmux' is currently not installed. You can install it by typing:
sudo apt install tmux
# install tmux
z1@z1-VirtualBox:~$ sudo apt install tmux
[sudo] password for z1: 
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following NEW packages will be installed:
  tmux
0 upgraded, 1 newly installed, 0 to remove and 47 not upgraded.
Need to get 223 kB of archives.
After this operation, 601 kB of additional disk space will be used.
Get:1 http://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial/main amd64 tmux amd64 2.1-3build1 [223 kB]
Fetched 223 kB in 0s (386 kB/s)
Selecting previously unselected package tmux.
(Reading database ... 217215 files and directories currently installed.)
Preparing to unpack .../tmux_2.1-3build1_amd64.deb ...
Unpacking tmux (2.1-3build1) ...
Processing triggers for man-db (2.7.5-1) ...
Setting up tmux (2.1-3build1) ...
```



### 3. Linux system

ctrl + H: show / hide the hidden files





### 4. Bash

```bash
# clear history
history -c && history -w

history
```

