- 分布式版本控制系统
- 版本控制系统：集中式（SVN）/分布式（git）
- 集中式控制系统：所有文件保存在中央服务器，每个人的电脑上保存着副本，但需要修改时，首先要从中央服务器上下载最新的版本，然后添加修改内容，修改完成后再上传到中央服务器。缺点上单点故障问题，中央服务器的故障是致命的
- 分布式版本控制系统：每个人的设备上都有一个完整的版本库，但需要分享内容给其他人时，只需要同步仓库内容即可
- Git工作流程图

Clone（克隆）：从远程仓库中克隆代码到本地仓库

Checkout（检出）：从本地仓库中检出一个仓库分支然后进行修订

add（添加）: 在提交前先将代码提交到暂存区

commit（提交）: 提交到本地仓库。本地仓库中保存修改的各个历史版本

fetch (抓取) ： 从远程库，抓取到本地仓库，不进行任何的合并动作，一般操作比较少。

pull (拉取) ： 从远程库拉到本地库，自动进行合并(merge)，然后放到工作区，相当于

fetch+merge

push（推送） : 修改完成后，需要和团队成员共享代码时，将代码推送到远仓库

- 简单Linux指令

ls/ll 查看当前目录

Cat 查看文件内容

Touch 创建文件

Vi vi编辑器

# 新建仓库

Repo-可以理解成目录，这个目录里所有的文件可以被git管理起来，每个文件的增删改操作都可以被Git跟踪到，以便任何时候都可以追踪历史或还原到之前的某一个版本

创建仓库的两种方式：

- Git init 在自己电脑本地直接创建一个仓库
- Git clone 从远程服务器上克隆一个已经存在的仓库

要使用Git对我们的代码进行版本控制，首先需要获得本地仓库

1）在电脑的任意位置创建一个空目录（例如test）作为我们的本地Git仓库

2）进入这个目录中，点击右键打开Git bash窗口

3）执行命令git init

4）如果创建成功后可在文件夹下看到隐藏的.git目录。

# Git的工作区域和文件状态

## 工作区域

- 工作区 Work Directory 电脑上的目录，资源管理器中能看到的文件夹就是工作区，实际操作的目录
- 暂存区 Staging Area/Index 临时存储区域，用于保存即将提交到git仓库的修改内容，版本控制的重要区域
- 本地仓库 Local repository Git存储代码和版本信息的主要位置

git -add 可以将修改的文件先添加到暂存区中

git -commit 一次性地将暂存区文件运送到本地仓库

## 文件状态

- 未跟踪 Untracked
- 未修改 Unmodified
- 已修改 modified
- 已暂存 Staged

# Git常用指令

1.  查看修改的状态（status）
	作用：查看修改的状态（暂存区、工作区）
	命令：`git status`

2.  添加工作区到暂存区（add）
	作用：添加工作区一个或多个文件的修改到暂存区
	命令形式：`git add 单个文件名|通配符`
	将所有修改加入暂存区：`git add .`

3.  提交到暂存区到本地仓库（commit）
	作用：提交到暂存区内容到本地仓库的当前分支
	命令形式：`git commit -m’注释内容’`

4.  查看提交日志（log）
	作用：查看提交记录
	命令形式：`git log[option]`
	Options：
		\--all 显示所有分支
		\--pretty=oneline 将提交信息显示为一行
		\--abbrev-commit 使得输出的commitid更简短
		\--graph 以图的形式显示

5.  版本回退
	作用：版本切换
	命令形式：`git reset --hard commitID`
	`commitID`可以使用git-log 或`git log`指令查看
	使用`HEAD`表示当前版本，上一个版本就是`HEAD~`
	回退到上一个版本`git reset --hard HEAD^`

- `git reset --soft`：回退到某一个版本，保留工作区和暂存区的所有内容
- `git reset --hard`：回退到某一个版本，丢弃工作区和暂存区的所有内容，一般决定放弃本地的所有修改内容时使用
- `git reset --mixed`：回退到某一个版本，只保留工作区的修改内容（reset的默认参数），执行get add 操作将变动过的内容重新添加到暂存区
- 查看已经删除的记录：`git reflog`

6.  gitignore文件

作用：一般我们总会有些文件无需纳入Git 的管理，也不希望它们总出现在未跟踪文件列表。 通常都是些自动生成的文件，比如日志文件，或者编译过程中创建的临时文件（字节码文件）等。 在这种情况下，我们可以在工作目录中创建一个名为 .gitignore 的文件（文件名称固定），列出要忽略的文件模式。

```gitignore
 # no .a files
 \*.a
 
 # but do track lib.a, even though you're ignoring .a files above
 !lib.a
 
 # only ignore the TODO file in the current directory, not subdir/TODO
 /TODO
 
 # ignore all files in the build/ directory
 build/
 
 # ignore doc/notes.txt, but not doc/server/arch.txt
 doc/\*.txt
 
 # ignore all .pdf files in the doc/ directory
 doc/\*\*/\*.pdf
 
```

# Git分支

几乎所有的版本控制系统都以某种形式支持分支。 使用分支意味着你可以把你的工作从开发主线上分离开来进行重大的Bug修改、开发新的功能，以免影响开发主线。

1.  查看本地分支

	命令：`git branch`

2.  创建本地分支

	命令：`git branch 分支名`

3.  切换分支（checkout）

	命令：`git checkout 分支名`

	还可以直接切换到一个不存在的分支（创建并切换）
	命令：`git checkout -b分支名`

4.  合并分支（merge）
	一个分支上的提交可以合并到另一个分支
	命令：git merge 分支名称

5.  删除分支
	不能删除当前分支，只能删除其他分支
	`git branch -d b1`删除分支时，需要做各种检查
	`git branch -D b1` 不做任何检查，强制删除

6.  解决冲突
	当两个分支上对文件的修改可能会存在冲突，例如同时修改了同一个文件的同一行，这时就需要手动解决冲突，解决冲突步骤：
	
	a. 处理文件中冲突的地方
	b. 将解决完冲突的文件加入暂存区(add)
	c. 提交到仓库(commit)

6.  开发中分支使用原则与流程
	在开发中，一般有如下分支使用原则与流程：
	master （生产） 分支 
		线上分支，主分支，中小规模项目作为线上运行的应用对应的分支；
	develop（开发）分支
		从master创建的分支，一般作为开发部门的主要开发分支，如果没有其他并行开发不同期上线要求，都可以在此版本进行开发，阶段开发完成后，需要合并到master分支,准备上线。
		
	feature/xxxx分支
		从develop创建的分支，一般是同期并行开发，但不同期上线时创建的分支，分支上的研发任务完成后合并到develop分支。
		
	hotfix/xxxx分支，
		从master派生的分支，一般作为线上bug修复使用，修复完成后需要合并到master、testdevelop分支。

还有一些其他分支，在此不再详述，例如test分支（用于代码测试）、pre分支（预上线分支）

```shell
 ###########################创建并切换到dev01分支，在dev01分支提交_
 # [master]创建分支dev01
  git branch dev01
  
  # [master]切换到dev01
  git checkout dev01
  
  # [dev01]创建文件file02.txt
 略
 
 # [dev01]将修改加入暂存区并提交到仓库,提交记录内容为：add file02 on dev
  git add .
  git commit -m 'add file02 on dev'
  
  # [dev01]以精简的方式显示提交记录
 git-log
 
  ###########################切换到master分支，将dev01合并到master分支
 # [dev01]切换到master分支
 git checkout master
 
  # [master]合并dev01到master分支
 git merge dev01
 
  # [master]以精简的方式显示提交记录
 git-log
 
 # [master]查看文件变化(目录下也出现了file02.txt)
 略
 
 ##########################删除dev01分支
 # [master]删除dev01分支
 git branch -d dev01
 
  # [master]以精简的方式显示提交记录
 git-log
```

# Git远程仓库

1.  配置SSH公钥
	生成SSH公钥
    `ssh-keygen -t rsa` 不断回车
    如果公钥已经存在，则自动覆盖
    
2. Gitee设置账户共公钥
	获取公钥 cat ~/.ssh/id_rsa.pub
	
3. 操作远程仓库
	- 添加远程仓库
		- 此操作是先初始化本地库，然后与已创建的远程库连接
		- 命令： `git remote add <远端名称> <仓库路径>`
			远端名称，默认是origin，取决于远端服务器设置 仓库路径，从远端服务器获取此URL
		- 例如:` git remote add origin git@gitee.com:czbk_zhang_meng/git_test.git`

	- 查看远程仓库
		命令：`git remote`
		
	- 推送到远程仓库
		命令：`git push [-f] [--set-upstream] [远端名称 [本地分支名][:远端分支名] ]`
		如果远程分支名和本地分支名称相同，则可以只写本地分支 `git push origin master`
		\-f 表示强制覆盖
		\--set-upstream 推送到远端的同时并且建立起和远端分支的关联关系。
			`git push --set-upstream origin master`
		如果当前分支已经和远端分支关联，则可以省略分支名和远端名。
			git push 将master分支推送到已关联的远端分支。

4.  本地分支与远程分支的关联关系
	查看关联关系我们可以使用
	`git branch -vv命令`

5.  从远程仓库克隆
	如果已经有一个远端仓库，我们可以直接clone到本地。
	命令: `git clone <仓库路径> [本地目录] 指定一个名字`
	本地目录可以省略，会自动生成一个目录

6.  从远程仓库中抓取和拉取
	远程分支和本地分支一样，我们可以进行merge操作，只是需要想把远端仓库里的更新都下载到本地，再进行操作
	- 抓取 命令：`git fetch [remote name] [branch name]`
		- 抓取指令就是将仓库里的更新都抓取到本地，不会进行合并
		- 如果不指定远端名称和分支名，则抓取所有分支。
	- 拉取命令：git pull \[remote name\] \[branch name\]
		- 拉取指令就是将远端仓库的修改拉到本地并自动进行合并，等同于fetch+merge
		- 如果不指定远端名称和分支名，则抓取所有并更新当前分支。

7.  解决合并冲突
	在一段时间，A、B用户修改了同一个文件，且修改了同一行位置的代码，此时会发生合并冲突。 A用户在本地修改代码后优先推送到远程仓库，此时B用户在本地修订代码，提交到本地仓库后，也需要推送到远程仓库，此时B用户晚于A用户，故需要先拉取远程仓库的提交，经过合并后才能推送到远端分支

# 在IDEA中使用Git

1.  创建项目远程仓库（gitee/github）
2.  初始化本地仓库，准备gitignore文件
	选择git仓库目录，默认是当前项目的目录

3.  设置远程仓库
	Mange remotes中输入远程仓库的地址

4.  提交到本地仓库
	Commit

5.  推送到远程仓库

	Push
	
 [在项目中解除idea与git的绑定](https://blog.csdn.net/m0_65992672/article/details/132338170)