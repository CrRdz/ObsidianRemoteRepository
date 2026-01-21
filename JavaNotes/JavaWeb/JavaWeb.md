

# JavaWeb综合案例

完成品牌数据的增删改查，批量删除，分页查询，条件查询

前端Vue Element + 后端MyBatis servlet

## 查询所有

Mapper-brandMapper.java

1.      @Select("select \* from tb_brand")
2.      @ResultMap（"brandResultMap"）
3.      List<Brand> selectAll();

由于Brand实体类中的名称与数据库表中字段不匹配，需要使用resultMap进行映射

resourses-com-itheima-mapper-brandMapper.xml

1.  <mapper namespace="com.itheima.mapper.BrandMapper">
2.      <resultMap id="brandResultMap" type="brand">
3.          <result property="brandName" column="brand_name" />
4.          <result property="companyName" column="company_name" />
5.      </resultMap>
6.  </mapper>

service-BrandMapper.java

创建一个接口，在接口中写方法

1.  List<Brand> selectAll();

service-impl-brandServiceImpl

1.  public class brandServiceImpl implements BrandService {
2.      _//1.创建sqlSessionFactory_
3.      SqlSessionFactory sqlSessionFactory = SqlSessionFactoryUtils.getSqlSessionFactory();
4.      @Override
5.      public List<Brand> selectAll() {

6.          _//2.获取SqlSession对象_
7.          SqlSession sqlSession = sqlSessionFactory.openSession();    

8.         _//3.获取BrandMapper_
9.         BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

10.         List<Brand> brands = mapper.selectAll();

11. _//5.释放资源_
12. sqlSession.close();
13.         return brands;

14.     }
15. }

通过接口-实现类，通过一些框架设计web层和service层可以解耦合

web-SelectAllServlet

1.  @WebServlet("/selectAllServlet")
2.  public class SelectAllServlet {

3.      private BrandService brandService = new brandServiceImpl();

4.      protected void doGet(HttpServletRequest request, HttpServletResponse response)
5.              throws ServletException, IOException {

6.         _//1. 调用service查询_
7.         List<Brand> brands = brandService.selectAll();

8.         _//2.转为json_
9.         String jsonString = JSON.toJSONString(brands);   

10.         _//3.写数据_
11.         response.setContentType("text/json;charset=utf-8");
12.         response.getWriter().write(jsonString);
13.     }

14.     protected void doPost(HttpServletRequest request, HttpServletResponse response)
15.             throws ServletException, IOException {
16. this.doGet(request, response);
17.     }
18. }

关于测试：Tomcat启程序，访问selectAllservlet，看到一系列的json数据则后台接收数据无误

\--后台代码#end

brand.html

1.      new Vue({
2.          el: "#app",

3.          mounted() {
4.              _//当页面加载完成后，发送异步请求_

5.              var \_this = this;

6.              axios({
7.                 method: "get",
8.                 url: "http://localhost:8080/brand-case/selectAllServlet"
9.             }).then(function(resp) {

10.                 \_this.tableData = resp.data;
11.             })

12.         },
13. }

当页面加载完成时候，发送异步请求来获取数据

通过then回调，获取响应，绑定function函数，resp.data就是列表数据，传到表格数据的模型上，this不能直接使用，声明提高级别

\--前端代码#end

## 新增品牌

Mapper-BrandMapper.java

1.      @Insert("insert into tb_brand values (null,#{brandName},#{companyName},#{ordered},#{description},#{status})")
2.      void add(Brand brand);

service-BrandMapper.java

1.  void add(Brand brand);

service-impl-BrandServiceImpl

1.      @Override
2.      public void add(Brand brand) {

3.          _//2.获取SqlSession对象_
4.          SqlSession sqlSession = sqlSessionFactory.openSession();

5.          _//3.获取BrandMapper_
6.          BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

7.         mapper.add(brand);

8.         _//4.提交事务_
9.         sqlSession.commit();

10.         _//5.释放资源_
11.         sqlSession.close();

12.     }

web-AddServlet

1.  @WebServlet("/addServlet")
2.  public class AddServlet {

3.      private BrandService brandService = new brandServiceImpl();

4.      protected void doGet(HttpServletRequest request, HttpServletResponse response)
5.              throws ServletException, IOException {

6.        _//1.接收品牌数据_
7.         BufferedReader br = request.getReader();
8.         String params = br.readLine();_//json字符串_

9.         _//2.转为brand对象_
10.         Brand brand = JSON.parseObject(params, Brand.class);

11.         _//3.调用service添加_
12.         brandService.add(brand);

13.         _//4.响应结果_
14.         response.getWriter().write("success");
15.     }

16.     protected void doPost(HttpServletRequest request, HttpServletResponse response)
17.             throws ServletException, IOException {
18. this.doGet(request, response);
19.     }
20. }

数据以json格式提交，使用request.getReader来获取消息体数据

\--后端代码#end

1.              <el-form-item>
2.                  <el-button type="primary" @click="addBrand">提交</el-button>
3.                  <el-button @click="dialogVisible = false">取消</el-button>
4.              </el-form-item>

静态页面表单的案件绑定，将按钮绑定单击事件addBrand

brand.html

1.              addBrand(){
2.                  _//console.log(this.brand);_

3.                  var \_this = this;

4.                  _//发送ajax异步请求_
5.                  axios({
6.                     method: "post",
7.                     url: "http://localhost:8080/brand-case/addServlet",
8.                    data: \_this.brand

9.                 }).then(function (resp){

10.                     _//添加成功_
11.                     if(resp.data() == "success"){

12.                         _//关闭窗口_
13.                         \_this.dialogVisible = false;

14.                         _//重新查询数据_                        
15.                         \_this.selectAll();

16.                         \_this.$message({
17.                             message: '添加成功',
18.                             type: 'success'
19.                         });

20.                     }
21.                 })
22.             },
23.                 })
24.             },

为了方便调用selectAll来展示数据，直接将selectAll封装成一个方法

1.   mounted() {this.selectAll()；},

可以加入’添加成功’提示框功能

前端代码#end

#修改品牌

#删除品牌

## Servlet代码优化

- Web层的Servlet个数太多，不利于管理和编写
- 将Servlet进行归类，对于同一个实体的操作方法，写到一个Servlet中，比如BrandServlet，UserServlet
- 不能继承HttpServlet，自定义Servlet，使用请求路径进行方法分发，替换HttpServlet的根据请求方式进行方法分发

反射调用：

1.  _/\*\*_
2.   \* 替换HttpServlet，根据请求的最后一段路径来进行方法分发
3.   \*/
4.  public class BaseServlet extends HttpServlet {
5.      @Override
6.      protected void service(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
7.          _//1.获取请求路径_
8.         String uri = req.getRequestURI();_// /brand-case/brand/selectAll_

9.         _//2.获取最后一段路径，方法名_
10.         int index = uri.lastIndexOf('/');_//获取最后一个/的位置_
11.         String methodName = uri.substring(index + 1);

12.         _//3.获取BrandServlet/UserServlet 字节码对象 class_
13.         _//谁调用我（this所在的方法），我（this）调用谁，这里的this指BrandServlet(baseServlet的子类们)，而不是Httpservlet_
14.         Class<? extends BaseServlet> cls = this.getClass();

15.         _//获取方法Method对象_
16.         try {
17.             Method method = cls.getMethod(methodName, HttpServletRequest.class, HttpServletResponse.class);
18.             _//执行方法_
19.             method.invoke(this,req,resp);

20.         }catch (NoSuchMethodException e){
21.             e.printStackTrace();
22.         } catch (InvocationTargetException e) {
23.             throw new RuntimeException(e);
24.         } catch (IllegalAccessException e) {
25.             throw new RuntimeException(e);
26.         }
27.     }
28. }

一个通用的 HttpServlet 替代类，用于根据 URL 路径动态调用子类中的方法。继承自 HttpServlet。然后重写父类 service() 方法，处理所有 HTTP 请求（GET、POST 等）。参数：req: 封装了客户端的请求信息。resp: 用于向客户端发送响应。再获取当前请求的 URI。当访问 /brand-case/brand/selectAll 时，得到字符串 /brand-case/brand/selectAll。找到最后一个斜杠 / 的位置，并提取其后的内容作为方法名。uri.substring(index + 1) 得到 "selectAll"。获取当前对象的实际运行时类的 Class 对象。如果当前是 BrandServlet 实例，则返回 BrandServlet.class。使用反射获取名为 methodName 的方法对象，要求该方法接受两个参数：HttpServletRequest 和 HttpServletResponse。使用反射调用该方法，并传入当前请求和响应对象。

对此前写的代码进行优化

1.  @WebServlet("/brand/\*")
2.  public class BrandServlet {

3.      private BrandService brandService = new brandServiceImpl();

4.      public void selectAll(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {}

5.      public void add(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException{}
6.  }

## 批量删除

Mapper-BrandMapper.java

1.      void deleteByIds(@Param("ids")int\[\] ids);

@Param("ids") 表示将方法参数 int\[\] ids 命名为 "ids"，以便在对应的 SQL 语句中引用。

当这个方法被调用时，传入的 ids 数组可以通过名称 "ids" 在 MyBatis 的 XML 映射文件或注解中的 SQL 语句里使用。

Resources-com-itheima-brandMapper.xml

1.      <delete id="delectByIds" >
2.          delete from tb_brand where in
3.          <foreach item="id" collection="ids" separator="," open="(" close=")">
4.              _#{id}_
5.          </foreach>
6.      </delete>

Sql语句复杂使用配置文件编写sql语句

service-BrandService.java

1.      void deleteByIds(int\[\] ids);

在接口中创建方法，接下来在实现类中实现该方法

service-BrandServiceImpl.java

1.      @Override
2.      public void deleteByIds(int\[\] ids) {

3.          _//2.获取SqlSession对象_
4.          SqlSession sqlSession = sqlSessionFactory.openSession();

5.          _//3.获取BrandMapper_
6.          BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

7.         mapper.deleteByIds(ids);

8.         _//4.提交事务_
9.         sqlSession.commit();

10.         _//5.释放资源_
11.         sqlSession.close();

12.     }

在实现类中调用方法

web-BrandServlet

1.      public void deleteByIds(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException{

2.          _//1.接收id数组\[1,2,3\]_
3.          BufferedReader br = request.getReader();
4.          String params = br.readLine();_//json字符串_

5.          _//2.转为int数组_
6.          int\[\] ids = JSON.parseObject(params, int\[\].class);

7.         _//3.调用service添加_
8.         brandService.deleteByIds(ids);

9.         _//4.响应结果_
10.         response.getWriter().write("success");
11.     }

\--后端代码#end

brand.html

1.  <el-button type="danger" plain @click="deleteByIds">批量删除</el-button>

静态页面，按键绑定deleteByIds事件，实现批量删除

1.              deleteByIds(){
2.                  _//1.创建id数组\[1,2,3\]_
3.                  for (let i = 0; i < this.multipleSelection.length; i++) {
4.                      let selectionElements = this.multipleSelection\[i\];
5.                      this.selectedIds\[i\] = selectionElements.id;
6.                  }

7.                  _//2.发送ajax异步请求_
8.                  axiosaxios({
9.                     method: "post",
10.                     url: "http://localhost:8080/brand-case/deleteByIds",
11.                     data: \_this.deleteByIds

12.                 }).then(function (resp){

13.                     _//删除成功_
14.                     if(resp.data() == "success"){

15.                         _//重新查询数据_
16.                         \_this.selectAll();

17.                         \_this.$message({
18.                             message: '添加成功',
19.                             type: 'success'
20.                         });
21.                     }
22.                 })
23.             }

创建方法deleteByIds，从multipleSelection中获取数据，并通过遍历，将数据存储到自建的selectedIds模型中

在data中新建一个selectedIds模型 id被选中，数组值发生变化，提交数据时提交数组到后台

1.                  //被选中的id数组
2.                  selectedIds:\[\],

优化：在删除时跳出确认框，确认是否删除

1.              _//批量删除_
2.              deleteByIds(){
3.                  _// 弹出确认提示框_

4.                  this.$confirm('此操作将删除该数据, 是否继续?', '提示', {
5.                      confirmButtonText: '确定',
6.                      cancelButtonText: '取消',
7.                      type: 'warning'
8.                  }).then(() => {
9.                     _//用户点击确认按钮_

10.                     _//1. 创建id数组 \[1,2,3\], 从 this.multipleSelection 获取即可_
11.                     for (let i = 0; i < this.multipleSelection.length; i++) {
12.                         let selectionElement = this.multipleSelection\[i\];
13.                         this.selectedIds\[i\] = selectionElement.id;

14.                     }

15.                     _//2. 发送AJAX请求_
16.                     var \_this = this;

17.                     _// 发送ajax请求，添加数据_
18.                     axios({
19.                         method:"post",
20.                         url:"http://localhost:8080/brand-case/brand/deleteByIds",
21.                         data:\_this.selectedIds
22.                     }).then(function (resp) {
23.                         if(resp.data == "success"){
24.                             _//删除成功_

25.                             _// 重新查询数据_
26.                             \_this.selectAll();
27.                             _// 弹出消息提示_
28.                             \_this.$message({
29.                                 message: '恭喜你，删除成功',
30.                                 type: 'success'
31.                             });

32.                         }
33.                     })
34.                 }).catch(() => {
35.                     _//用户点击取消按钮_

36.                     this.$message({
37.                         type: 'info',
38.                         message: '已取消删除'
39.                     });
40.                 });

41.             }

用then catch包裹两种条件

\--前端代码#end

## 分页查询

- 分页查询LIMIT，参数1：开始索引，参数2：查询的条目数

SELECT \* FROM tb_brand LIMIT 0,5

- 页面（前端）传递的参数- 当前页码currentPage 与 每页查询的条目数pageSize
- 后台返回的数据- 当前页数据 List 与 总记录数 totalCount
- 开始索引 = （当前页数-1）\* 每页显示条数
- 查询条目数 = 查询的条目数 = 每页显示条数

Pojo-PageBean

1.  _//分页查询的JavaBean_
2.  public class PageBean<T> {
3.      _// 总记录数_
4.      private int totalCount;
5.      _// 当前页数据_
6.      private List<T> rows;

7.      public int getTotalCount() {
8.         return totalCount;
9.     }

10.     public void setTotalCount(int totalCount) {
11.         this.totalCount = totalCount;
12.     }

13.     public List<T> getRows() {
14.         return rows;
15.     }

16.     public void setRows(List<T> rows) {
17.         this.rows = rows;
18.     }
19. }

实体类中定义bean，泛型声明一个T，可以让代码通用，在pagebean中存放总记录数与当前页数据，并设置getter/setter方法

Mapper-BrandMapper.java

1.  _/\*\*_
2.       \* 分页查询
3.       \* @param begin
4.       \* @param size
5.       \* @return
6.       \*/
7.      @Select("select \* from tb_brand limit #{begin} , #{size}")
8.      @ResultMap("brandResultMap")
9.      List<Brand> selectByPage(@Param("begin") int begin,@Param("size") int size);

10.     _/\*\*_
11.      \* 查询总记录数
12.      \* @return
13.      \*/
14.     @Select("select count(\*) from tb_brand ")
15. @ResultMap("brandResultMap")
16.     int selectTotalCount();

BrandService.java

1.      _/\*\*_
2.       \* 分页查询
3.       \* @param currentPage  当前页码
4.       \* @param pageSize   每页展示条数
5.       \* @return
6.       \*/
7.      PageBean<Brand>  selectByPage(int currentPage,int pageSize);

返回一个Pagebean对象，由前端传入currentPage和pageSize

Service-impl-brandServiceImpl.java

1.  @Override
2.      public PageBean<Brand> selectByPage(int currentPage, int pageSize) {
3.          _//2. 获取SqlSession对象_
4.          SqlSession sqlSession = factory.openSession();
5.          _//3. 获取BrandMapper_
6.          BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

7.          _//4. 计算开始索引_
8.         int begin = (currentPage - 1) \* pageSize;
9.         _// 计算查询条目数_
10.         int size = pageSize;

11.         _//5. 查询当前页数据_
12.         List<Brand> rows = mapper.selectByPage(begin, size);

13.         _//6. 查询总记录数_
14.         int totalCount = mapper.selectTotalCount();

15.         _//7. 封装PageBean对象_
16.         PageBean<Brand> pageBean = new PageBean<>();
17.         pageBean.setRows(rows);
18.         pageBean.setTotalCount(totalCount);

19.         _//8. 释放资源_
20.         sqlSession.close();

21.         return pageBean;
22.     }

BrandServlet.java

1.  public void selectByPage(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
2.          _//1. 接收 当前页码 和 每页展示数    url?currentPage=1&pageSize=5_
3.          String \_currentPage = request.getParameter("currentPage");
4.          String \_pageSize = request.getParameter("pageSize");

5.          int currentPage = Integer.parseInt(\_currentPage);
6.          int pageSize = Integer.parseInt(\_pageSize);

7.          _//2. 调用service查询_
8.         PageBean<Brand> pageBean = brandService.selectByPage(currentPage, pageSize);

9.         _//2. 转为JSON_
10.         String jsonString = JSON.toJSONString(pageBean);
11.         _//3. 写数据_
12.         response.setContentType("text/json;charset=utf-8");
13.         response.getWriter().write(jsonString);
14.     }

请求中接收的类型是String类型，而查询中需要的为int类型，所以需要强制转换

后端代码#end

brand.html

1.              selectAll(){

2.                  var \_this = this;

3.                  axios( {
4.                      method: "post",
5.                      url: "http://localhost:8080/brand-case/brand/selectByPage?currentPage=" + \_this.currentPage + "&pageSize="+ \_this.pageSize,

6.                 }).then(function(resp){
7.                     \_this.tableData = resp.data.rows;
8.                     \_this.totalCount = resp.data.totalCount;
9.                     console.log(resp.data);
10.                 })

11.             },

因为修改分页查询，相当于修改了selectAll的显示方式，此前是加载完成之后就执行selectAll，这里url直接使用拼字符串的方式，将tableData模型数据设置成rows即当前页的数据，totalCount为页的数量，也建立到一个模型中。通过响应到的数据来为这两个模型设置值

在data中设置模型：pageSize，totalCount和currentPage其中5，100为默认值

1.                  _//每页显示的条数_
2.                  pageSize:5,
3.                  _//总记录数_
4.                  totalCount:100,
5.                  _// 当前页码_
6.                  currentPage: 1,

分页工具条

1.      <!--分页工具条-->
2.      <el-pagination
3.              @size-change="handleSizeChange"
4.              @current-change="handleCurrentChange"
5.              :current-page="currentPage"
6.              :page-sizes="\[5, 10, 15, 20\]"
7.              :page-size="5"
8.              layout="total, sizes, prev, pager, next, jumper"
9.              :total="totalCount">
10.     </el-pagination>

Total处展示总记录数，建立到totalCount模型中，@size-change，@current-change是动态分页的方法

动态分页

1.    _//分页_
2.              handleSizeChange(val) {
3.                  _// console.log(\`每页 ${val} 条\`);_
4.                  _//重新设置每页显示的条数_
5.                  this.pageSize = val;
6.                  this.selectAll();
7.              },
8.              handleCurrentChange(val) {
9.                  _//console.log(\`当前页: ${val}\`);_

10.                 _//重新设置当前页码_
11.                 this.currentPage = val;
12.                 this.selectAll();
13.             },

Val用来接收分页工具栏停留的位置，以及需要显示的数量

前端代码#end

## 条件查询

需要完成条件查询，并且按照分页的形式展示

BrandMapper.java

1.      _/\*\*_
2.       \* 分页条件查询
3.       \* @param begin
4.       \* @param size
5.       \* @return
6.       \*/
7.      List<Brand> selectByPageAndCondition(@Param("begin") int begin, @Param("size") int size, @Param("brand") Brand brand);

8.      _/\*\*_
9.      \* 根据条件查询总记录数
10.      \* @return
11.      \*/

12.     Integer selectTotalCountByCondition(Brand brand);

使用Integer即使查询结果为空，MyBatis 也能安全地返回 null，而不会引发类型不匹配异常

BrandMapper.xml

1.      <select id="selectByPageAndCondition" resultMap="brandResultMap">
2.          select \*
3.          from tb_brand
4.          <where>
5.          <if test=" brandName != null and  brandName ！=''">
6.              and brand_name like _#{ brandName}_
7.          </if>

8.          <if test=" companyName != null and  companyName ！=''">
9.             and company_name like _#{ companyName}_
10.         </if>

11.         <if test=" status != null ">
12.             and status = _#{ status}_
13.         </if>

14.         </where>

15.         limit _#{begin},#{size}_
16.     </select>

17.     <select id="selectTotalCountByCondition" resultMap="brandResultMap">
18.         select count(\*)
19.         from tb_brand
20.         <where>
21.             <if test=" brandName != null and  brandName ！=''">
22.                 and brand_name like _#{ brandName}_
23.             </if>

24.             <if test=" companyName != null and  companyName ！=''">
25.                 and company_name like _#{ companyName}_
26.             </if>

27.             <if test=" status != null ">
28.                 and status = _#{ status}_
29.             </if>

30.         </where>

31.     </select>

由于需要写动态SQL，所以在XML文件中编辑，第二个select语句中，由于没有采用@brand注解，可以直接使用brand实体类中的属性，所以可以省略brand. ，同时希望模糊匹配没使用like，而不是=

BrandService.java

1.  PageBean<Brand> selectByPageAndCondition(int currentPage, int pageSize, Brand brand);

分页条件查询，返回一个pageBean

BrandServiceImpl.java

1.      @Override
2.      public PageBean<Brand> selectByPageAndCondition(int currentPage, int pageSize, Brand brand) {

3.          _//2.获取SqlSession对象_
4.          SqlSession sqlSession = factory.openSession();

5.          _//3.获取BrandMapper_
6.          BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

7.         _//计算开始索引_
8.         int begin = (currentPage-1) \* pageSize;
9.         _//计算查询条目数_
10.         int size = pageSize;

11.         _//处理brand条件，模糊表达式_
12.         String brandName = brand.getBrandName();
13.         if(brandName != null && brandName.length() > 0){
14.             brand.setBrandName("%" + brandName + "%");
15.         }

16.         String companyName = brand.getCompanyName();
17.         if(companyName != null && companyName.length() > 0){
18.             brand.setCompanyName("%" + companyName + "%");
19.         }

20.         _//4.查询当前页数据_
21.         List<Brand> rows = mapper.selectByPageAndCondition(begin, size,brand);

22.         _//5.查询总记录数_
23.         int totalCount = mapper.selectTotalCountByCondition(brand);

24.         PageBean<Brand> pageBean = new PageBean<>();
25.         pageBean.setRows(rows);
26.         pageBean.setTotalCount(totalCount);

27.         sqlSession.close();

28.         return pageBean;
29.     }

新增处理brand对象，使模糊表达式，对用户的输入封装成模糊表达式的形式

BrandServlet.java

1.      public void selectByPageAndCondition(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
2.          _//1. 接收两个参数 currentPage pageSize_
3.          String \_currentPage = request.getParameter("currentPage");
4.          String \_pageSize = request.getParameter("pageSize");

5.          _//获取查询条件对象_
6.          BufferedReader br = request.getReader();
7.          String params = br.readLine();_//json字符串_

8.         Brand brand = JSON.parseObject(params, Brand.class);

9.         int currentPage = Integer.parseInt(\_currentPage);
10.         int pageSize = Integer.parseInt(\_pageSize);

11.         PageBean<Brand> pageBean = brandService.selectByPageAndCondition(currentPage, pageSize,brand);

12.         _//转为json_
13.         String json = JSON.toJSONString(pageBean);
14.         response.setContentType("text/json;charset=utf-8");
15.         response.getWriter().write(json);
16.     }

Brand的数据通过前端传递，将method改为post方式，使用data来传递，接收请求体的参数，currentPage和pageSize使用url来传递

后端代码#end

Brand.html

1.              _//查询所有_
2.              selectAll(){

3.                  var \_this = this;

4.                  axios( {
5.                      method: "post",
6.                      url: "http://localhost:8080/brand-case/brand/selectByPageAndCondition?currentPage=" + \_this.currentPage + "&pageSize="+ \_this.pageSize,
7.                      data:this.brand

8.                 }).then(function(resp){
9.                     \_this.tableData = resp.data.rows;
10.                     \_this.totalCount = resp.data.totalCount;
11.                     console.log(resp.data);
12.                 })

13.             },
14.             onSubmit() {
15.                 console.log(this.brand);
16.                 this.selectAll()
17.             },

将请求改为post形式，并使用data将brand传入selectAll中，查询按键绑定onSubmit事件，点击时调用selectAll方法

前端代码优化

Var \_this = this 使用麻烦

使用=>箭头函数，不用再使用_this

1.  axios({
2.                      method:"post",
3.                      url:"http://localhost:8080/brand-case/brand/selectByPageAndCondition?currentPage="+this.currentPage+"&pageSize="+this.pageSize,
4.                      data:this.brand
5.                  }).then(resp =>{
6.                      _//设置表格数据_
7.                      this.tableData = resp.data.rows; _// {rows:\[\],totalCount:100}_
8.                      _//设置总记录数_
9.                      this.totalCount = resp.data.totalCount;
10.                 })

\--前端代码#end

# SSM

Spring +SpringMVC +Mybatis

Dao=Mapper

domain=pojo

git clone git@github.com:CrRdz/Learning_SSM.git

## Spring

- Spring技术是JavaEE开发的必备技术，企业开发技术选型命中率>90%
- 简化开发，框架整合（MyBatis/Struts/Hibernate）
- Spring发展到今天已经形成一种开发生态圈，Spring提供若干个项目，每个项目用于完成特定的功能

### Spring Framework

Spring Framework是Spring生态中最基础的项目，是其他项目的根基

#### 系统架构

架构上层依赖于下层

底层：

Core Container 核心容器（beans Core Context SpEL）

中层：

AOP（面向切面编程）Aspects（AOP思想实现）

上层：

Data Access/Integration数据访问/集成（JDBC ORM OXM JMS Transaction事务）

Web Web开发（WebSocket Servlet Web Portlet）

#### 核心概念

- 代码书写现状：耦合度偏高

|

解决方案：使用对象时，在程序中不要主动使用new产生新对象，转换为由外部提供对象

数据层实现

1.  public class BookDaoImpl implements BookDao {
2.      public void save() {
3.          System.out.println("book dao save ...");
4.      }
5.  }

6.  public class BookDaoImpl2 implements BookDao {
7.      public void save() {
8.          System.out.println("book dao save ...2");
9.      }
10.  }

业务层实现

1.  public class BookServiceImpl implements BookService {
2.      private BookDao bookDao = new BookDaoImpl2;
3.      public void save() {
4.          bookDao.save();
5.      }
6.  }

如果数据层出现了一个新的实现类，因为业务层需要创建新的对象，BookDaoImpl改成BookDaoImpl2那么需要重新编译，重新部署...

那么不实现对象，就可以降低耦合

- IoC（Inversion of Control）控制反转：对象的创建控制权由程序转移到外部的思想

它将对象的创建和依赖关系的管理交给Spring框架，而不是在代码中手动创建对象。这种设计思想可以降低代码的耦合度，提高代码的可维护性和可测试性。

- Spring提供了一个IoC容器，用来充当IoC思想的外部

|

负责对象的创建，初始化等一系列工作

被IoC容器创建或管理的对象在IoC容器中统称为bean

- DI（Dependency Injection）依赖注入

|

在容器中建立bean与bean之间的依赖关系的整个过程（service依赖于dao 绑定service和dao）

- 目标：充分解耦

使用IoC容器管理bean（IoC）在容器中将有依赖关系的bean进行关系绑定（DI）使用对象时不仅可以直接从IoC容器中直接获取，并且获取到的bean已经绑定了所有依赖关系

#### 核心容器

##### IoC快速入门

- 管理Service与Dao
- 通过配置文件的方式将被管理的对象告知IoC容器
- 被管理的对象交给IoC通过接口获取到IoC容器
- IoC容器得到后，通过接口方法中获取bean

准备：

定义spring管理的类

导包spring-context 导入坐标

pom.xml

1.      <dependency>
2.        <groupId>org.springframework</groupId>
3.        <artifactId>spring-context</artifactId>
4.        <version>5.2.10.RELEASE</version>
5.      </dependency>

创建配置文件将被管理的对象告知IoC容器

resouse中创建spring.config配置文件xml 配置对应类作为Spring管理的bean

ApplicationContext.xml

1.      _<!--1.导入spring的坐标spring-context，对应版本是5.2.10.RELEASE-->_

2.      _<!--2.配置bean-->_
3.      _<!--bean标签标示配置bean_
4.      id属性标示给bean起名字
5.      class属性表示给bean定义类型-->
6.      <bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl"/>

7.      <bean id="bookService" class="com.itheima.service.impl.BookServiceImpl"/>

围堵标签或者空标签皆可

App2.java

获取IoC容器 初始化IoC容器，通过容器获取bean

1.  public class App2 {
2.      public static void main(String\[\] args) {
3.          _//3.获取IoC容器_
4.          ApplicationContext ctx = new ClassPathXmlApplicationContext("applicationContext.xml");
5.          _//4.获取bean（根据bean配置id获取）_
6.  _//        BookDao bookDao = (BookDao) ctx.getBean("bookDao");_
7.  _//        bookDao.save();_

8.          BookService bookService = (BookService) ctx.getBean("bookService");
9.         bookService.save();

10.     }
11. }

##### DI快速入门

- 基于IoC管理bean
- Service中使用new形式创建的Dao对象不保留
- Service中需要的Dao对象通过提供方法进入到Service中
- Service与Dao之间的关系用配置文件描述

BookServiceImpl.java

1.  public class BookServiceImpl implements BookService {
2.      _//5.删除业务层中使用new的方式创建的dao对象_
3.      private BookDao bookDao;

4.      public void save() {
5.          System.out.println("book service save ...");
6.          bookDao.save();
7.      }
8.      _//6.提供对应的set方法_
9.     public void setBookDao(BookDao bookDao) {
10.         this.bookDao = bookDao;
11.     }
12. }

applicationContext

1.      <bean id="bookService" class="com.itheima.service.impl.BookServiceImpl">
2.          _<!--7.配置server与dao的关系-->_
3.          _<!--property标签表示配置当前bean的属性_
4.          name属性表示配置哪一个具体的属性
5.          ref属性表示参照哪一个bean-->
6.          <property name="bookDao" ref="bookDao"/>
7.      </bean>

Ref-reference

Dao告知service关系 对service修改

Service中有个属性是bookDao 对应需要参照的对象bookDao（id）两个bookDao并不是一个

##### Bean-IoC

1.  Bean配置

- Bean基础配置
- Bean别名配置
- Bean作用范围配置

基础配置:

功能：定义Spring核心容器管理的对象

格式

1.  <beans>
2.      <bean/>
3.      <bean></bean>
4.  </beans>

属性列表:

Id：bean的id，使用容器可以通过id值获取对应的bean，在一个容器中id值唯一

Class：bean的类型，即配置的bean的全路径名

别名配置

1.      _<!--name:为bean指定别名，别名可以有多个，使用逗号，分号，空格进行分隔-->_
2.      <bean id="bookService" name="service service4 bookEbi" class="com.itheima.service.impl.BookServiceImpl">
3.          <property name="bookDao" ref="bookDao"/>
4.      </bean>

使用name属性配置 但还是建议使用id引用

Bean作用范围

1.      _<!--scope：为bean设置作用范围，可选值为单例singloton，非单例prototype-->_
2.      <bean id="bookDao" name="dao" class="com.itheima.dao.impl.BookDaoImpl" scope="prototype"/>

为了控制同一个bean是不是同一个bean对象，即是否为单例，同一个为单例

Singleton：单例（默认）

Prototype：非单例

为什么bean默认为单例？

\--因为希望对象是可以复用的

适合交给容器进行管理的bean

\-表现层对象

\-业务层对象

\-数据层对象

\-工具对象

不适合交给容器管理的bean

\-封装实体的域对象

1.  Bean实例化

- Bean如何创建
- Bean创建的三种形式

1.  提供可访问的构造方法

Bean本质上就是对象，创建bean使用构造方法完成

BookDaoImpl.java

1.  public class BookDaoImpl implements BookDao {

2.      public BookDaoImpl() {
3.          System.out.println("book dao constructor is running ....");
4.      }

5.      public void save() {
6.          System.out.println("book dao save ...");
7.      }
8. }

无参构造方法如果不存在，将抛出BeanCreationException

配置

1.  _<!--方式一：构造方法实例化bean-->_
2.  <bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl"/>

3.  通过静态工厂

现在不常用，一般为兼容早期遗留系统

AppForInstanceOrder.java

1.  public class AppForInstanceOrder {
2.      public static void main(String\[\] args) {
3.          _//通过静态工厂创建对象_

4.          ApplicationContext ctx = new ClassPathXmlApplicationContext("applicationContext.xml");

5.          OrderDao orderDao = (OrderDao) ctx.getBean("orderDao");

6.          orderDao.save();

7.     }
8. }

OrderDaoFactory.java

1.  public class OrderDaoFactory {
2.      public static OrderDao getOrderDao(){
3.          System.out.println("factory setup....");
4.          return new OrderDaoImpl();
5.      }
6.  }

配置

1.      _<!--方式二：使用静态工厂实例化bean-->_
2.  <bean id="orderDao" class="com.itheima.factory.OrderDaoFactory" factory-method="getOrderDao"/>

Class是工厂类名，如果不加factory-method 那么配出来的bean是工厂的实例对象，还需要加上工厂内路径

1.  使用实例工厂

相对于静态工厂更为繁琐

1.  public class AppForInstanceUser {
2.      public static void main(String\[\] args) {
3.          _//创建实例工厂对象_
4.          UserDaoFactory userDaoFactory = new UserDaoFactory();
5.          _//通过实例工厂对象创建对象_
6.          UserDao userDao = userDaoFactory.getUserDao();
7.          userDao.save();
8.      }
9.  }

创建实例工厂对象，通过实例工厂对象创建对象

UserDaoFactory.java

1.  _//实例工厂创建对象_
2.  public class UserDaoFactory {
3.      public UserDao getUserDao(){
4.          return new UserDaoImpl();
5.      }
6.  }

配置

1.      _<!--方式三：使用实例工厂实例化bean-->_
2.  <bean id="userFactory" class="com.itheima.factory.UserDaoFactory"/>
3.  <bean id="userDao" factory-method="getUserDao" factory-bean="userFactory"/>

需要先造出工厂对象 工厂中的路径是getUserDao方法 工厂对象对应的bean使用工厂id

1.  使用factoryBean（方式C的变种）
2.  public class UserDaoFactoryBean implements FactoryBean<UserDao> {
3.      _//代替原始实例工厂中创建对象的方法_
4.      public UserDao getObject() throws Exception {
5.          return new UserDaoImpl();
6.      }

7.      public Class<?> getObjectType() {
8.          return UserDao.class;
9.     }
10. }

需要实现FactoryBean 泛型中写需要实例化的对象

配置

1.     _<!--方式四：使用FactoryBean实例化bean-->_
2.     <bean id="userDao" class="com.itheima.factory.UserDaoFactoryBean"/>

配置时更简单

默认的对象是单例的，通过override一个isSingleton方法 通过修改true-单例 和false-非单例切换，一般不用刻意书写

1.  Bean的生命周期

- 生命周期：从创建到消亡的完整过程
- Bean生命周期：bean从创建到销毁的整体过程

1.  初始化容器

创建对象（内存分配）-执行构造方法-执行属性注入（set操作）-执行bean初始化方法

1.  使用bean

执行业务操作

1.  关闭/销毁容器

执行bean销毁方法

- Bean生命周期控制：在bean创建到销毁前做一些事情

BookDaoImpl.java

1.  public class BookDaoImpl implements BookDao {
2.      public void save() {
3.          System.out.println("book dao save ...");
4.      }
5.      _//表示bean初始化对应的操作_
6.      public void init(){
7.          System.out.println("init...");
8.      }
9.      _//表示bean销毁前对应的操作_
10.     public void destory(){
11.         System.out.println("destory...");
12.     }

13. }

配置

1.      _<!--init-method：设置bean初始化生命周期回调函数-->_
2.      _<!--destroy-method：设置bean销毁生命周期回调函数，仅适用于单例对象-->_
3.      <bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl" init-method="init" destroy-method="destory"/>

4.  public class AppForLifeCycle {
5.      public static void main( String\[\] args ) {
6.          ClassPathXmlApplicationContext ctx = new ClassPathXmlApplicationContext("applicationContext.xml");

7.          BookDao bookDao = (BookDao) ctx.getBean("bookDao");
8.          bookDao.save();
9.          _//注册关闭钩子函数，在虚拟机退出之前回调此函数，关闭容器_
10.          _//ctx.registerShutdownHook();_
11.          _//关闭容器_
12.         ctx.close();
13.     }
14. }

registerShutdownHook在虚拟机退出之前回调此函数关闭容器

Close相对更暴力

但实际开发中，关闭容器应伴随Tomcat

使用接口控制生命周期

1.  public class BookServiceImpl implements BookService, InitializingBean, DisposableBean {
2.      private BookDao bookDao;

3.      public void setBookDao(BookDao bookDao) {
4.          System.out.println("set .....");
5.          this.bookDao = bookDao;
6.      }

7.      public void save() {
8.         System.out.println("book service save ...");
9.         bookDao.save();
10.     }

11.     public void destroy() throws Exception {
12.         System.out.println("service destroy");
13.     }

14.     public void afterPropertiesSet() throws Exception {
15.         System.out.println("service init");
16.     }
17. }

这样可以省略配置文件中的init-method...

Bean销毁时机

容器关闭前触发bean的销毁

关闭容器方法：手工关闭容器/注册关闭钩子，在虚拟机退出前关闭容器再退出虚拟机

##### 依赖注入方式-DI

Dependency-Injection

- 向一个类中传递数据的方式：普通方法（set）/构造方法
- 依赖注入描述了在容器中建立Bean与bean之间依赖关系的过程，当处理数字或字符串时，需要区分类型，引用类型/简单类型（基本数据类型与String）
- 依赖注入方式：

Setter注入：简单类型/引用类型

构造器注入：简单类型/引用类型

1.  Setter注入

空参

- 引用类型

BookServiceImpl.java

1.  public class BookServiceImpl implements BookService{
2.      private BookDao bookDao;
3.      private UserDao userDao;
4.      _//setter注入需要提供要注入对象的set方法_
5.      public void setUserDao(UserDao userDao) {
6.          this.userDao = userDao;
7.      }
8.      _//setter注入需要提供要注入对象的set方法_
9.      public void setBookDao(BookDao bookDao) {
10.         this.bookDao = bookDao;
11.     }

12.     public void save() {
13.         System.out.println("book service save ...");
14.         bookDao.save();
15.         userDao.save();
16.     }
17. }

applicationContext

1.      _<!--注入引用类型-->_
2.      <bean id="bookService" class="com.itheima.service.impl.BookServiceImpl">
3.          _<!--property标签：设置注入属性-->_
4.          _<!--name属性：设置注入的属性名，实际是set方法对应的名称-->_
5.          _<!--ref属性：设置注入引用类型bean的id或name-->_
6.          <property name="bookDao" ref="bookDao"/>
7.          <property name="userDao" ref="userDao"/>
8.      </bean>

- 简单类型

BookDaoImpl.java

1.  public class BookDaoImpl implements BookDao {

2.      private String databaseName;
3.      private int connectionNum;
4.      _//setter注入需要提供要注入对象的set方法_
5.      public void setConnectionNum(int connectionNum) {
6.          this.connectionNum = connectionNum;
7.      }
8.      _//setter注入需要提供要注入对象的set方法_
9.     public void setDatabaseName(String databaseName) {
10.         this.databaseName = databaseName;
11.     }
12.     public void save() {
13.         System.out.println("book dao save ..."+databaseName+","+connectionNum);
14.     }
15. }

applicationContext

1.      _<!--注入简单类型-->_
2.      <bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl">
3.          _<!--property标签：设置注入属性-->_
4.          _<!--name属性：设置注入的属性名，实际是set方法对应的名称-->_
5.          _<!--value属性：设置注入简单类型数据值-->_
6.          <property name="connectionNum" value="100"/>
7.          <property name="databaseName" value="mysql"/>
8.      </bean>

提供可访问的set方法

配置中使用property标签value属性注入简单类型数据

1.  构造器注入

- 引用类型

BookServiceImpl.java

1.  public class BookServiceImpl implements BookService{
2.      private BookDao bookDao;
3.      private UserDao userDao;

4.      public BookServiceImpl(BookDao bookDao, UserDao userDao) {
5.          this.bookDao = bookDao;
6.          this.userDao = userDao;
7.      }

8.     public void save() {
9.         System.out.println("book service save ...");
10.         bookDao.save();
11.         userDao.save();
12.     }
13. }

ApplicationContext

1.      <bean id="bookService" class="com.itheima.service.impl.BookServiceImpl">
2.          <constructor-arg name="userDao" ref="userDao"/>
3.          <constructor-arg name="bookDao" ref="bookDao"/>
4.      </bean>

- 简单类型

1.  public class BookDaoImpl implements BookDao {
2.      private String databaseName;
3.      private int connectionNum;

4.      public BookDaoImpl(String databaseName, int connectionNum) {
5.          this.databaseName = databaseName;
6.          this.connectionNum = connectionNum;
7.      }

8.     public void save() {
9.         System.out.println("book dao save ..."+databaseName+","+connectionNum);
10.     }
11. }

applicationContext

1.      <bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl">
2.          <constructor-arg name="connectionNum" value="10"/>
3.          <constructor-arg name="databaseName" value="mysql"/>
4.      </bean>

5.  问题

耦合度高 applicationContext与BookDaoImpl耦合度高 如果形参名称更改，applicaton中constructor-arg中的name属性也要同步修改

1.  _<!--解决形参名称的问题，与形参名不耦合 根据构造方法类型注入-->_
2.  <bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl">
3.          <constructor-arg type="int" value="10"/>
4.          <constructor-arg type="java.lang.String" value="mysql"/>
5.  </bean>

6.  _<!--解决参数类型重复问题，使用位置解决参数匹配-->_
7.      <bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl">
8.          _<!--根据构造方法参数位置注入-->_
9.          <constructor-arg index="0" value="mysql"/>
10.          <constructor-arg index="1" value="100"/>
11.      </bean>

12.  依赖注入方式选择

- 强制依赖使用构造器，使用setter注入有概率不进行注入导致null对象出现
- 可选依赖使用setter注入进行，灵活性强
- Spring框架倡导使用构造器，第三方内部大多数采用构造器注入的形式进行数据初始化，相对严谨
- 如果有必要可以两者同时使用，使用构造器注入完成强制依赖注入，使用setter注入完成可选依赖注入
- 实际开发中还需要根据实际情况分析，如果受控对象没有提供setter方法就必须使用构造器注入
- 自己开发的模块推荐使用setter注入

##### 依赖自动装配

IoC容器根据bean所依赖的资源在容器中自动查找并注入bean中的过程称为自动装配

自动装配方式：按类型/按名称/按构造方法/不启用自动装配

1.  <bean id="bookDao" class="com.itheima.service.impl.BookDaoImpl" />
2.  _<!--autowire属性：开启自动装配，通常使用按类型装配-->_
3.  <bean id="bookService" class="com.itheima.service.impl.BookServiceImpl" autowire="byType"/>

按类型装配时，bean对象需唯一 连id都可以省略

如果有两个实现类-按名称装配，但是耦合度高

- 依赖自动装配特征

1.  自动装配用于引用类型依赖注入，不能对简单类型进行操作
2.  使用按类型装配时必须保障容器中相同类型的bean唯一推荐使用
3.  使用按名称装配时必须保障容器中具有指定名称的bean，变量名与配置名耦合高
4.  自动装配优先级低于setter注入与构造器注入，同时出现时自动装配配置失效

##### 集合注入

数组/List/Set/Map/Properties

1.  public class BookDaoImpl implements BookDao {

2.      private int\[\] array;
3.      private List<String> list;
4.      private Set<String> set;
5.      private Map<String,String> map;
6.      private Properties properties;

7.      public void setArray(int\[\] array) {
8.         this.array = array;
9.     }
10.     public void setList(List<String> list) {
11.         this.list = list;
12.     }
13.     public void setSet(Set<String> set) {
14.         this.set = set;
15.     }
16.     public void setMap(Map<String, String> map) {
17.         this.map = map;
18.     }
19.     public void setProperties(Properties properties) {
20.         this.properties = properties;
21.     }
22.     public void save() {
23.         System.out.println("book dao save ...");
24.         System.out.println("遍历数组:" + Arrays.toString(array));
25.         System.out.println("遍历List" + list);
26.         System.out.println("遍历Set" + set);
27.         System.out.println("遍历Map" + map);
28.         System.out.println("遍历Properties" + properties);
29.     }
30. }

配置

1.  <bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl">
2.          _<!--数组注入-->_
3.          <property name="array">
4.              <array>
5.                  <value>100</value>
6.                  <value>200</value>
7.                  <value>300</value>
8.              </array>
9.          </property>
10.         _<!--list集合注入-->_
11.         <property name="list">
12.             <list>
13.                 <value>itcast</value>
14.                 <value>itheima</value>
15.                 <value>boxuegu</value>
16.                 <value>chuanzhihui</value>
17.             </list>
18.         </property>
19.         _<!--set集合注入-->_
20.         <property name="set">
21.             <set>
22.                 <value>itcast</value>
23.                 <value>itheima</value>
24.                 <value>boxuegu</value>
25.                 <value>boxuegu</value>
26.             </set>
27.         </property>
28.         _<!--map集合注入-->_
29.         <property name="map">
30.             <map>
31.                 <entry key="country" value="china"/>
32.                 <entry key="province" value="henan"/>
33.                 <entry key="city" value="kaifeng"/>
34.             </map>
35.         </property>
36.         _<!--Properties注入-->_
37.         <property name="properties">
38.             <props>
39.                 <prop key="country">china</prop>
40.                 <prop key="province">henan</prop>
41.                 <prop key="city">kaifeng</prop>
42.             </props>
43.         </property>
44.     </bean>

注：

Set如果重复会自动过滤

Array与list能混用

<ref bean = “beanId’’> 如果使用引用类型

##### 案例：数据源对象管理

导入坐标

配置数据源对象作为spring管理的bean

管理第三方数据连接池

1.  _<!--    管理DruidDataSource对象-->_
2.     <bean id ="dataSouce" class="com.alibaba.druid.pool.DruidDataSource">
3.          <property name="driverClassName" value="com.mysql.jdbc.Driver"/>
4.          <property name="url" value="jdbc:mysql://localhost:3306/spring_db"/>
5.          <property name="username" value="root"/>
6.          <property name="password" value="root"/>
7.     </bean>

管理c3p0

1.      <bean id="dataSource" class="com.mchange.v2.c3p0.ComboPooledDataSource">
2.          <property name="driverClass" value="com.mysql.jdbc.Driver"/>
3.          <property name="jdbcUrl" value="jdbc:mysql://localhost:3306/spring_db"/>
4.          <property name="user" value="root"/>
5.          <property name="password" value="root"/>
6.          <property name="maxPoolSize" value="1000"/>
7.      </bean>

使用setter注入

##### 加载properties文件

1.  <beans xmlns="http://www.springframework.org/schema/beans"
2.         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
3.         xmlns:context="http://www.springframework.org/schema/context"
4.         xsi:schemaLocation="
5.              http://www.springframework.org/schema/beans
6.              http://www.springframework.org/schema/beans/spring-beans.xsd
7.              http://www.springframework.org/schema/context
8.              http://www.springframework.org/schema/context/spring-context.xsd
9.              ">
10. 开启一个全新的context命名空间
11. 使用context空间加载properties文件
12. 使用属性占位符${}读取properties文件中的属性
13. <context:property-placeholder location="jdbc.properties">
14.     <bean class="com.alibaba.druid.pool.DruidDataSource">
15.         <property name="driverClassName" value="${jdbc.driver}"/>
16.         <property name="url" value="${jdbc.url}"/>
17.         <property name="username" value="${jdbc.username}"/>
18.         <property name="password" value="${jdbc.password}"/>
19.     </bean>

不加载系统变量system-properties-mode="NEVER"

加载多个properties使用通配符

Classpath\*表示不仅可以从当前目录读取也可以读取框架中jar包，设置加载当前工程类路径和当前工程所依赖的所有jar包中的所有properties文件

1.  <context:property-placeholder location="classpath\*:\*.properties" system-properties-mode="NEVER"/>

##### 容器补充

- 创建容器
- 方式一：类路径加载配置文件
- 方式二：文件路径加载配置文件
- 获取bean
- 方式一：使用bean名称获取，强转
- 方式二：使用bean名称获取并指定类型
- 方式三：使用bean类型获取，容器中这个类型的bean只能有一个

1.  public class App {
2.      public static void main(String\[\] args) {
3.          _//1.加载类路径下的配置文件_
4.          ApplicationContext ctx = new ClassPathXmlApplicationContext("applicationContext.xml");
5.          _//2.从文件系统下加载配置文件_
6.  _//        ApplicationContext ctx = new FileSystemXmlApplicationContext("D:\\\\workspace\\\\spring\\\\spring_10_container\\\\src\\\\main\\\\resources\\\\applicationContext.xml");_
7.  _//        BookDao bookDao = (BookDao) ctx.getBean("bookDao");_
8.  _//        BookDao bookDao = ctx.getBean("bookDao",BookDao.class);_
9.  _//        BookDao bookDao = ctx.getBean(BookDao.class);_
10. _//        bookDao.save();_
11.     }
12. }

- 容器类层次结构

顶层接口beanFactory

- BeanFactory

1.  _//初始化BeanFactory_
2.  public class AppForBeanFactory {
3.      public static void main(String\[\] args) {
4.          Resource resources = new ClassPathResource("applicationContext.xml");
5.          BeanFactory bf = new XmlBeanFactory(resources);
6.  _//        BookDao bookDao = bf.getBean(BookDao.class);_
7.  _//        bookDao.save();_
8.      }
9.  }

Beanfactory与applicationContext加载bean的实际不一样，beanFactory是延迟加载bean（懒汉），application是立即加载bean（饿汉）

1.  <bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl" lazy-init="true"/>

在配置文件中加入这一行，也可以使application延迟加载

##### 核心容器总结

1.  容器相关

BeanFactory是IoC的顶层接口，初始化BeanFactory对象时，加载的bean延迟加载

ApplicationContext接口是Spring容器的核心接口，初始化bean立即加载

ApplicationContext接口提供基础的bean操作相关方法，通过其他接口扩展其功能

ApplicationContext接口常用初始化类：

ClassPathXmlApplicationContext，FileSystemXmlApplicationContext

1.  Bean相关

Bean的id

Bean别名

Bean类型，静态工厂类，factoryBean类

控制bean的实例数量

生命周期初始化方法

生命周期销毁方法

自动装配类型

Bean工厂方法，应用于静态工厂或实例工厂

实例工厂bean

控制bean延迟加载

1.  依赖注入相关

构造器注入引用类型

构造器注入简单类型

类型匹配与索引匹配

Setter注入引用类型

Setter注入简单类型

List集合

集合注入简单类型

集合注入引用类型

#### 注解开发

##### 注解开发定义bean

使用@Component定义bean

1.  _//@Component定义bean_
2.  @Component("bookDao")
3.  public class BookDaoImpl implements BookDao {
4.      public void save() {
5.          System.out.println("book dao save ...");
6.      }
7.  }

8.  _//@Component定义bean_
9.  @Component
10.  public class BookServiceImpl implements BookService {
11.      private BookDao bookDao;

12.      public void setBookDao(BookDao bookDao) {
13.          this.bookDao = bookDao;
14.      }

15.     public void save() {
16.         System.out.println("book service save ...");
17.         bookDao.save();
18.     }
19. }

Component可以指定名称理解成id

核心配置文件中通过组件扫描加载bean

1.  <context:component-scan base-package="com.itheima"/>

Spring提供@Component注解的三个衍生注解，功能完全一致，方便理解

业务层@Service

数据层@Repository

表现层@Controller

##### 纯注解开发

- Spring3.0升级了纯注解开发模式，使用java类替代配置文件，开启Spring快速开发赛道
- 读取Spring核心配置文件初始化容器对象切换为Java配置类初始化容器对象

新建config包下建SpringConfig类

1.  _//声明当前类为Spring配置类_
2.  @Configuration
3.  _//设置bean扫描路径，多个路径书写为字符串数组格式_
4.  @ComponentScan({"com.itheima.service","com.itheima.dao"})
5.  public class SpringConfig {
6.  }

作用完全替代：applicationContext

@ComponentScan注解用于设定扫描路径，此诸结只能添加一次，多个数据用数组格式

修改：

ApplicationContext ctx = new AnnotationConfigApplicationContext(SpringConfig.class);

1.  public class AppForAnnotation {
2.      public static void main(String\[\] args) {
3.          _//AnnotationConfigApplicationContext加载Spring配置类初始化Spring容器_
4.          ApplicationContext ctx = new AnnotationConfigApplicationContext(SpringConfig.class);
5.          BookDao bookDao = (BookDao) ctx.getBean("bookDao");
6.          System.out.println(bookDao);
7.          _//按类型获取bean_
8.          BookService bookService = ctx.getBean(BookService.class);
9.          System.out.println(bookService);
10.     }
11. }

##### Bean管理

1.  bean作用范围
2.  @Repository
3.  _//@Scope设置bean的作用范围_
4.  @Scope("singleton")
5.  public class BookDaoImpl implements BookDao {

6.      public void save() {
7.          System.out.println("book dao save ...");
8.      }
9. }

10.  Bean生命周期
11.      _//@PostConstruct设置bean的初始化方法_
12.      @PostConstruct
13.      public void init() {
14.          System.out.println("init ...");
15.      }
16.      _//@PreDestroy设置bean的销毁方法_
17.      @PreDestroy
18.      public void destroy() {
19.         System.out.println("destroy ...");
20.     }

##### 依赖注入

自动装配

1.  @Service
2.  public class BookServiceImpl implements BookService {
3.      _//@Autowired：注入引用类型，自动装配模式，默认按类型装配_
4.      @Autowired
5.      private BookDao bookDao;
6.      public void save() {
7.          System.out.println("book service save ...");
8.          bookDao.save();
9.      }
10. }

可以去除setter注入，直接使用Autowired注解，自动装配基于反射设计创建对象并暴力反射对应属性为私有属性初始化数据

自动装配建议使用无参构造方法创建对象

当有两个实现类时候，按名称注入 开启指定名称装配bean

1.  _//@Qualifier：自动装配bean时按bean名称装配_
2.  @Qualifier("bookDao")

但是这个注解必须依赖@Autowired

注入简单类型

1.  @Repository("bookDao")
2.  public class BookDaoImpl implements BookDao {
3.      _//@Value：注入简单类型（无需提供set方法）_
4.      @Value("${name}")
5.      private String name;

6.      public void save() {
7.          System.out.println("book dao save ..." + name);
8.      }
9. }

配置文件

1.  @Configuration
2.  @ComponentScan("com.itheima")
3.  _//@PropertySource加载properties配置文件_
4.  @PropertySource({"jdbc.properties"})
5.  public class SpringConfig {
6.  }

写多个properties配置文件，使用数组

@PropertySource({"jdbc.properties","jdbc.properties","jdbc.properties"})

这里不支持通配符，仅支持单一文件配置

##### 第三方bean管理

1.  第三方bean管理
2.  public class SpringConfig {
3.      _//1.定义一个方法获得要管理的对象_
4.      _//2.添加@Bean，表示当前方法的返回值是一个bean_
5.      _//@Bean修饰的方法，形参根据类型自动装配_
6.      @Bean
7.      public DataSource dataSource(BookDao bookDao){

8.          DruidDataSource ds = new DruidDataSource();
9.         ds.setDriverClassName("com.mysql.jdbc.Driver");
10.         ds.setUrl("jdbc:mysql://localhost:3306/spring_db");
11.         ds.setUsername("root");
12.         ds.setPassword("root");
13.         return ds;
14.     }
15. }

16.  public class App {
17.      public static void main(String\[\] args) {
18.          AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext(SpringConfig.class);
19.          DataSource dataSource = ctx.getBean(DataSource.class);
20.          System.out.println(dataSource);
21.      }
22.  }

问题：耦合度高

解决：新建jdbc.config

1.  @Configuration配置JdbcConfig
2.  @Configuration
3.  public class JdbcConfig {
4.      _//1.定义一个方法获得要管理的对象_
5.      _//2.添加@Bean，表示当前方法的返回值是一个bean_
6.      _//@Bean修饰的方法，形参根据类型自动装配_
7.      @Bean
8.      public DataSource dataSource(BookDao bookDao){

9.         DruidDataSource ds = new DruidDataSource();
10.         ds.setDriverClassName("com.mysql.jdbc.Driver");
11.         ds.setUrl("jdbc:mysql://localhost:3306/spring_db");
12.         ds.setUsername("root");
13.         ds.setPassword("root");
14.         return ds;
15.     }
16. }

扫描config

1.  @Configuration
2.  @ComponentScan("com.itheima.config")
3.  public class SpringConfig {
4.  }

问题：不知道导入的是哪个配置，如果配置文件很多时

1.  Import
2.  @Configuration
3.  @ComponentScan("com.itheima")
4.  _//@Import:导入配置信息_
5.  @Import({JdbcConfig.class})
6.  public class SpringConfig {
7.  }

并取消@Configuration配置jdbc

1.  第三方bean依赖注入

简单类型注入

1.  public class JdbcConfig {
2.      _//1.定义一个方法获得要管理的对象_
3.      @Value("com.mysql.jdbc.Driver")
4.      private String driver;
5.      @Value("jdbc:mysql://localhost:3306/spring_db")
6.      private String url;
7.      @Value("root")
8.      private String userName;
9.      @Value("root")
10.     private String password;
11.     _//2.添加@Bean，表示当前方法的返回值是一个bean_
12.     _//@Bean修饰的方法_
13.     @Bean
14.     public DataSource dataSource(){
15.         DruidDataSource ds = new DruidDataSource();
16.         ds.setDriverClassName(driver);
17.         ds.setUrl(url);
18.         ds.setUsername(userName);
19.         ds.setPassword(password);
20.         return ds;
21.     }
22. }

引用类型注入

1.      _//@Bean修饰的方法，形参根据类型自动装配_
2.      @Bean
3.      public DataSource dataSource(BookDao bookDao){
4.          System.out.println(bookDao);
5.          DruidDataSource ds = new DruidDataSource();
6.          ds.setDriverClassName(driver);
7.          ds.setUrl(url);
8.          ds.setUsername(userName);
9.          ds.setPassword(password);
10.         return ds;
11.     }
12. }

放在形参列表中，按类型自动装配

##### 注解开发总结

XML配置vs注解开发

<div class="joplin-table-wrapper"><table><tbody><tr><td><p>功能</p></td><td><p>XML配置</p></td><td><p>注解</p></td></tr><tr><td><p>定义bean</p></td><td><p>Bean标签</p><ul><li>Id属性</li><li>Class属性</li></ul></td><td><p>@Component</p><p>@Controller</p><p>@Service</p><p>@Repository</p><p>@ComponentScan</p></td></tr><tr><td><p>设置依赖注入</p></td><td><p>Setter注入</p><p>构造器注入</p><p>自动装配</p></td><td><p>@Autowired</p><p>@Qualifier</p><p>@Value</p></td></tr><tr><td><p>配置第三方bean</p></td><td><p>Bean标签</p><p>静态工厂，实例工厂，FactoryBean</p></td><td><p>@Bean</p></td></tr><tr><td><p>作用范围</p></td><td><p>Scope属性</p></td><td><p>@scope</p></td></tr><tr><td><p>生命周期</p></td><td><p>标准接口</p><ul><li>init-method</li><li>destory-method</li></ul></td><td><p>@PostConstructor</p><p>@PreDestory</p></td></tr></tbody></table></div>

#### 整合

##### Spring整合MyBatis

1.  MyBatis核心流程分析
2.          _// 1. 创建SqlSessionFactoryBuilder对象_
3.          SqlSessionFactoryBuilder sqlSessionFactoryBuilder = new SqlSessionFactoryBuilder();
4.          _// 2. 加载SqlMapConfig.xml配置文件_
5.          InputStream inputStream = Resources.getResourceAsStream("SqlMapConfig.xml.bak");
6.          _// 3. 创建SqlSessionFactory对象_
7.          SqlSessionFactory sqlSessionFactory = sqlSessionFactoryBuilder.build(inputStream);
8.          _// 4. 获取SqlSession_
9.          SqlSession sqlSession = sqlSessionFactory.openSession();
10.         _// 5. 执行SqlSession对象执行查询，获取结果User_
11.        AccountDao accountDao = sqlSession.getMapper(AccountDao.class);

12.         _// 6. 释放资源_
13.         sqlSession.close();

初始化SqlSessionFactory - 获取连接，获取实现 - 获取数据层接口 - 关闭连接

核心对象：SqlSessionFactory

SqlMapConfig

1.  <configuration>
2.      <properties resource="jdbc.properties"></properties>
3.      <typeAliases>
4.          <package name="com.itheima.domain"/>
5.      </typeAliases>
6.      <environments default="mysql">
7.          <environment id="mysql">
8.              <transactionManager type="JDBC"></transactionManager>
9.              <dataSource type="POOLED">
10.                 <property name="driver" value="${jdbc.driver}"></property>
11.                 <property name="url" value="${jdbc.url}"></property>
12.                 <property name="username" value="${jdbc.username}"></property>
13.                 <property name="password" value="${jdbc.password}"></property>
14.             </dataSource>
15.         </environment>
16.     </environments>
17.     <mappers>
18.         <package name="com.itheima.dao"></package>
19.     </mappers>
20. </configuration>

整合MyBatis

初始化属性数据 - 初始化类别别名 - 初始化dataSource - 初始化映射配置

1.  整合MyBatis

准备：

额外导包

1.      <dependency>
2.        <groupId>org.springframework</groupId>
3.        <artifactId>spring-jdbc</artifactId>
4.        <version>5.2.10.RELEASE</version>
5.      </dependency>

6.      <dependency>
7.        <groupId>org.mybatis</groupId>
8.        <artifactId>mybatis-spring</artifactId>
9.       <version>1.3.0</version>
10.     </dependency>

SpringConfig

1.  @Configuration
2.  @ComponentScan("com.itheima")
3.  _//@PropertySource：加载类路径jdbc.properties文件_
4.  @PropertySource("classpath:jdbc.properties")
5.  @Import({JdbcConfig.class,MybatisConfig.class})
6.  public class SpringConfig {
7.  }

JdbcConfig

1.  public class JdbcConfig {
2.      @Value("${jdbc.driver}")
3.      private String driver;
4.      @Value("${jdbc.url}")
5.      private String url;
6.      @Value("${jdbc.username}")
7.      private String userName;
8.      @Value("${jdbc.password}")
9.      private String password;

10.     @Bean
11.     public DataSource dataSource(){
12.         DruidDataSource ds = new DruidDataSource();
13.         ds.setDriverClassName(driver);
14.         ds.setUrl(url);
15.         ds.setUsername(userName);
16.         ds.setPassword(password);
17.         return ds;
18.     }
19. }

准备#end

在SqlMapConfig中的所有操作都是为了SqlSessionFactory准备

所以要在SqlSessionFactorybean中管理

1.  public class MybatisConfig {
2.      _//定义bean，SqlSessionFactoryBean，用于产生SqlSessionFactory对象_
3.      @Bean
4.      public SqlSessionFactoryBean sqlSessionFactory(DataSource dataSource){
5.          SqlSessionFactoryBean ssfb = new SqlSessionFactoryBean();
6.          ssfb.setTypeAliasesPackage("com.itheima.domain");
7.          ssfb.setDataSource(dataSource);
8.          return ssfb;
9.      }
10.     _//定义bean，返回MapperScannerConfigurer对象_
11.     @Bean
12.     public MapperScannerConfigurer mapperScannerConfigurer(){
13.         MapperScannerConfigurer msc = new MapperScannerConfigurer();
14.         msc.setBasePackage("com.itheima.dao");
15.         return msc;
16.     }
17. }

完全替代

1.      <typeAliases>
2.          <package name="com.itheima.domain"/>
3.      </typeAliases>
4.      <environments default="mysql">
5.          <environment id="mysql">
6.              <transactionManager type="JDBC"></transactionManager>
7.              <dataSource type="POOLED">
8.                  <property name="driver" value="${jdbc.driver}"></property>
9.                  <property name="url" value="${jdbc.url}"></property>
10.                 <property name="username" value="${jdbc.username}"></property>
11.                 <property name="password" value="${jdbc.password}"></property>
12.             </dataSource>
13.         </environment>
14.     </environments>
15.     <mappers>
16.         <package name="com.itheima.dao"></package>
17.     </mappers>

只需要配置不是默认的部分

2.Line1-3对应1.Line6

2.Line15-17对应1.Line14

1.Line7使用形参注入引用类型，引用JdbcConfig中的dataSouce （bean）

1.      <mappers>
2.          <package name="com.itheima.dao"></package>
3.      </mappers>

对于这一段与SqlSession不是一体的，SqlSessionFactoryBean只负责造出SqlSession

##### Spring整合JUnit

src\\test\\java\\com\\itheima\\service\\AccountServiceTest.java

1.  _//设置类运行器_
2.  @RunWith(SpringJUnit4ClassRunner.class)
3.  _//设置Spring环境对应的配置类_
4.  @ContextConfiguration(classes = SpringConfig.class)
5.  public class AccountServiceTest {
6.      _//支持自动装配注入bean_
7.      @Autowired
8.      private AccountService accountService;

9.     @Test
10.     public void testFindById(){
11.         System.out.println(accountService.findById(1));

12.     }

13.     @Test
14.     public void testFindAll(){
15.         System.out.println(accountService.findAll());
16.     }
17. }

使用Spring整合Junit专用的类加载器

#### AOP

##### AOP简介

- AOP（Aspect Oriented Programming）面向切面编程，一种编程范式，知道开发者如何组织程序结构
- 作用：在不惊动原始设计（不需要修改源代码）的基础上为其进行功能增强
- Spring理念：无入侵式编程

##### AOP核心概念

原始方法称为连接点

需要追加功能的称为切入点

共性功能，需要被追加的操作叫通知

- 连接点（JoinPoint）：程序执行过程中的任意位置，粒度为执行方法，抛出异常，设置变量，在SpringAOP中，；理解为方法的执行
- 切入点（PointCut）：匹配连接点的式子，在SpringAOP中，一个切入点可以只描述一个具体方法，也可以匹配多个方法
- 一个具体方法：com.itheima.dao包下的BookDao接口中无形参无返回值的save方法
- 匹配多个方法：所有的save方法，所有的get开头的方法，所有以Dao结尾的接口中的任意方法，所有带有一个参数的方法
- 通知（advice）：在切入点执行的操作，也就是共性功能，在SpringAOP中，功能以方法的形式呈现
- 通知类：定义通知的类
- 切面（Aspect）：描述通知与切入点的对应关系

##### AOP入门案例

1.  AOP入门案例思路分析

案例设定：测定接口执行效率

简化设定：在接口执行前输出当前系统时间

开发模式：注解

1.  AOP入门案例实现

- 导入坐标（pom.xml）

1.      <dependency>
2.        <groupId>org.springframework</groupId>
3.        <artifactId>spring-context</artifactId>
4.        <version>5.2.10.RELEASE</version>
5.      </dependency>
6.      <dependency>
7.        <groupId>org.aspectj</groupId>
8.        <artifactId>aspectjweaver</artifactId>
9.        <version>1.9.4</version>
10.     </dependency>

- 制作连接点方法（原始操作，Dao接口与实现类）
- 制作共性功能（通知类与通知）

1.      public void method(){
2.          System.out.println(System.currentTimeMillis());
3.      }

- 定义切入点@Pointcut("execution(void com.itheima.dao.BookDao.update())")

切入点定义依托一个不具有实际意义的方法进行，即无参数，无返回值，方法体无实际逻辑

- 绑定切入点与通知关系（切面）_@Before("pt()")_

aop-Myadvice

1.  _//通知类必须配置成Spring管理的bean_
2.  @Component
3.  _//设置当前类为切面类_
4.  @Aspect
5.  public class MyAdvice {
6.      _//设置切入点，要求配置在方法上方_
7.      @Pointcut("execution(void com.itheima.dao.BookDao.update())")
8.      private void pt(){}

9.     _//设置在切入点pt()的前面运行当前操作（前置通知）_
10. @Before("pt()")
11.     public void method(){
12.         System.out.println(System.currentTimeMillis());
13.     }
14. }

配置@EnableAspectJAutoProxy

1.  @Configuration
2.  @ComponentScan("com.itheima")
3.  _//开启注解开发AOP功能_
4.  @EnableAspectJAutoProxy
5.  public class SpringConfig {
6.  }

开启注解式AOP注解驱动支持

##### AOP工作流程

1.  Spring容器启动
2.  读取所有切面配置中的切入点
3.  初始化bean，判定bean对应的类中的方法是否匹配任意切入点

匹配失败，创建对象

匹配成功，创建原始对象（目标对象）的代理对象

1.  获取bean执行方法

获取bean，调用方法并执行，完成操作

获取的bean是代理对象时，根据代理对象的运行模式运行原始方法与增强的内容，完成操作

注：

目标对象：原始功能去掉共性功能对应的类产生的对象，这种对象是无法直接完成最终工作

代理：目标对象无法直接完成工作，需要对其功能回填，通过原始对象的代理对象实现

##### AOP切入点表达式

切入点：需要增强的方法

切入点表达式：要进行增强的方法的描述方式

描述方式一：执行com.itheima.dao包下的BookDao接口中的无参数update方法

@Pointcut("execution(void com.itheima.dao.BookDao.update())")

描述方式二：执行com.itheima.dao.impl包下的BookDaoImpl类中的无参数update方法

@Pointcut("execution(void com.itheima.dao.impl.BookDaoImpl.update())")

切入点表达式标准格式：

动作关键字（访问修饰符 返回值 包名.类/接口名.方法名（参数）异常名）

动作关键字：例如execution表示执行到指定切入点

访问修饰符：public/private 可以省略

1.  使用通配符描述切入点，快速描述

\*：单个独立的任意符号，可以独立出现，也可以作为前缀或者后缀的匹配符出现

execution(public \* com.itheima.\*.UserService.find\*(\*))

匹配com.itheima包下的任意包中的UserService类或接口中所有find开头的带有一个参数的方法

..：多个连续的任意符号，可以独立出现，常用于简化包名与参数的书写

execution(public User com..UserService.findById(..))

匹配com包下的任意包中的UserService类或接口中所有名称为findById的方法

+：专用于匹配子类类型

execution(\* \*..Service+.\*(..))

匹配任意业务层方法

1.  书写技巧

- 所有代码按照标准规范开发
- 描述切入点通常描述接口，而不描述实现类（耦合）
- 访问控制修饰符针对接口开发均采用public（可省略）
- 返回值类型对于增删改查类使用精准类型加速匹配，对于查询类使用\*快速描述
- 包名书写尽量不适用..匹配，效率过低，常用\*做单个包描述匹配，或精准匹配
- 接口名/类名书写名称与模块相关的采用\*匹配，例如UserService书写成\*Service,绑定业务层接口名
- 方法名书写以动词进行精准匹配，名词采用\*匹配，例如getById书写成getBy\*，selectAll书写成select\*
- 参数规则较为复杂，根据业务方法灵活调整
- 通常不使用异常作为匹配规则

##### AOP通知类型

- AOP通知类型描述了抽取的共性功能，根据共性功能抽取的位置不同，最终运行代码时要将其加入合理的位置
- AOP通知共分为5种类型
- 前置通知
- 后置通知

1.      @Pointcut("execution(void com.itheima.dao.BookDao.update())")
2.      private void pt(){}
3.      @Pointcut("execution(int com.itheima.dao.BookDao.select())")
4.      private void pt2(){}

5.      _//@Before：前置通知，在原始方法运行之前执行_
6.  @Before("pt()")
7.      public void before() {
8.          System.out.println("before advice ...");
9.     }

10.     _//@After：后置通知，在原始方法运行之后执行_
11. @After("pt2()")
12.     public void after() {
13.         System.out.println("after advice ...");
14.     }

输出结果

before advice ...

book dao update is running ...

after advice...

- 环绕通知

1.      @Around("pt()")
2.      public void around(ProceedingJoinPoint pjp) throws Throwable {
3.          System.out.println("around before advice ...");
4.          _//表示对原始操作的调用_
5.          pjp.proceed();
6.          System.out.println("around after advice ...");
7.      }

抛出异常是因为无法预期原始操作是否存在异常

标准写法

1.      @Around("pt()")
2.      public Object around(ProceedingJoinPoint pjp) throws Throwable {
3.          System.out.println("around before advice ...");
4.          _//表示对原始操作的调用_
5.          Object ret = pjp.proceed();
6.          System.out.println("around after advice ...");
7.          return ret;
8.      }

- 对原始方法调用可直接返回值ret

@Around注意事项

- 环绕通知需要依赖形参ProceedingJoinPoint才能实现对原始方法的调用，进而实现原始方法调用前后同时添加通知
- 通知中如果未使用ProceedingJoinPoint对原始方法进行调用将跳过原始方法的执行
- 对原始方法的调用可以不接受返回值，通知方法设置成void即可，如果接收返回值，必须设定为Object类型
- 由于无法预知原始方法运行后是否会抛出异常，因此环绕通知方法必须抛出Throwable对象

- 返回后通知

1.      _//@AfterReturning：返回后通知，在原始方法执行完毕后运行，且原始方法执行过程中未出现异常现象_
2.      @AfterReturning("pt2()")
3.      public void afterReturning() {
4.          System.out.println("afterReturning advice ...");
5.      }

- 抛出异常后通知

1.      _//@AfterThrowing：抛出异常后通知，在原始方法执行过程中出现异常后运行_
2.      @AfterThrowing("pt2()")
3.      public void afterThrowing() {
4.          System.out.println("afterThrowing advice ...");
5.      }
6.  }

##### 案例：测量业务层接口万次执行效率

需求：任意业务层接口执行均可显示其执行效率（执行时长）

分析

业务功能：业务层接口执行前后分别记录时间，求差值得到执行效率

通知类型选择前后均可增强的类型--环绕通知

配置

1.  @Configuration
2.  @ComponentScan("com.itheima")
3.  @PropertySource("classpath:jdbc.properties")
4.  @Import({JdbcConfig.class,MybatisConfig.class})
5.  @EnableAspectJAutoProxy
6.  public class SpringConfig {
7.  }

ProjectAdvice

1.  @Component
2.  @Aspect
3.  public class ProjectAdvice {
4.      _//匹配业务层的所有方法_
5.      @Pointcut("execution(\* com.itheima.service.\*Service.\*(..))")
6.      private void servicePt(){}

7.      _//设置环绕通知，在原始操作的运行前后记录执行时间_
8.      @Around("ProjectAdvice.servicePt()")
9.     public void runSpeed(ProceedingJoinPoint pjp) throws Throwable {
10.         _//获取执行的签名对象_
11.         Signature signature = pjp.getSignature();
12.         String className = signature.getDeclaringTypeName();
13.         String methodName = signature.getName();

14.         long start = System.currentTimeMillis();
15.         for (int i = 0; i < 10000; i++) {
16.            pjp.proceed();
17.         }

18.         long end = System.currentTimeMillis();
19.         System.out.println("万次执行："+ className+"."+methodName+"---->" +(end-start) + "ms");
20.     }
21. }

注：

模拟当前测试的接口执行效率仅仅是一个理论值，并不是一次完整的执行过程

##### AOP通知获取数据

- 获取切入点方法参数
- JoinPoint：适用于前置后置返回后抛出异常后通知

1.      _//JoinPoint：用于描述切入点的对象，必须配置成通知方法中的第一个参数，可用于获取原始方法调用的参数_
2.      @Before("pt()")
3.      public void before(JoinPoint jp) {
4.          Object\[\] args = jp.getArgs();
5.          System.out.println(Arrays.toString(args));
6.          System.out.println("before advice ..." );
7.      }

8.      @After("pt()")
9.     public void after(JoinPoint jp) {
10.         Object\[\] args = jp.getArgs();
11.         System.out.println(Arrays.toString(args));
12.         System.out.println("after advice ...");
13.     }

- ProceedJointPoint：适用于环绕通知

1.      @Around("pt()")
2.      public Object around(ProceedingJoinPoint pjp) {
3.          Object\[\] args = pjp.getArgs();
4.          System.out.println(Arrays.toString(args));
5.          args\[0\] = 666;
6.          Object ret = pjq.proceed(args);
7.          return ret;
8.      }

args可以先处理传入的参数，保证健壮性

- 获取返回值
- 返回后通知

1.      _//设置返回后通知获取原始方法的返回值，要求returning属性值必须与方法形参名相同_
2.      @AfterReturning(value = "pt()",returning = "ret")
3.      public void afterReturning(JoinPoint jp,String ret) {
4.          System.out.println("afterReturning advice ..."+ret);
5.      }

JoinPoint如有必须放第一个

- 环绕方法

1.      @Around("pt()")
2.      public Object around(ProceedingJoinPoint pjp) {
3.          Object\[\] args = pjp.getArgs();
4.          System.out.println(Arrays.toString(args));
5.          args\[0\] = 666;
6.          Object ret = pjq.proceed(args);
7.          return ret;
8.      }

- 获取异常
- 抛出异常后通知 使用形参接收对应的异常对象

1.      _//设置抛出异常后通知获取原始方法运行时抛出的异常对象，要求throwing属性值必须与方法形参名相同_
2.      @AfterThrowing(value = "pt()",throwing = "t")
3.      public void afterThrowing(Throwable t) {
4.          System.out.println("afterThrowing advice ..."+t);
5.      }

- 环绕通知

1.      @Around("pt()")
2.      public Object around(ProceedingJoinPoint pjp) {
3.          Object\[\] args = pjp.getArgs();
4.          System.out.println(Arrays.toString(args));
5.          args\[0\] = 666;
6.          Object ret = null;
7.          try {
8.              ret = pjp.proceed(args);
9.          } catch (Throwable t) {
10.             t.printStackTrace();
11.         }
12.         return ret;
13.     }

##### 案例：百度网盘密码数据兼容处理

分析：

在业务方法执行之前对所有输入参数进行格式处理-trim()

使用处理后参数调用原始方法-环绕通用之中存在对原始方法的调用

DataAdvice

1.  @Component
2.  @Aspect
3.  public class DataAdvice {
4.     @Pointcut("execution(boolean com.itheima.service.\*Service.\*(\*,\*))")
5.      private void servicePt(){}

6.      @Around("DataAdvice.servicePt()")
7.      public Object trimStr(ProceedingJoinPoint pjp) throws Throwable {
8.          Object\[\] args = pjp.getArgs();
9.         for (int i = 0; i < args.length; i++) {
10.             _//判断参数是不是字符串_
11.             if(args\[i\].getClass().equals(String.class)){
12.                 args\[i\] = args\[i\].toString().trim();
13.             }
14.         }
15.         Object ret = pjp.proceed(args);
16.         return ret;
17.     }

18. }

##### AOP总结

- 概念：面向切面编程，一种编程范式
- 作用：在不惊动原始设计的基础上为方法进行功能增强
- 核心概念
- 代理（Proxy）：SpringAOP中理解为任意方法的执行
- 连接点（JoinPoint）：在SpringAOP中，理解为任意方法的执行
- [切入点（PointCut）](#_AOP切入点表达式)：匹配连接点的式子，也有具有共性功能的方法描述
- [通知（Advice）](#_AOP通知类型)：若干个方法的共性功能，在切入点处执行，最终体现为一个方法
- 切面（Aspect）：描述通知与切入点的对应关系
- 目标对象（Target）：被代理的原始对象成为目标对象

#### 事务

- 事务作用：在数据层保障一系列数据库操作同成功同失败
- Spring事务作用：在数据层保障一系列数据库操作同成功同失败

##### Spring事务简介

案例：模拟银行将转账业务

需求：实现任意两个账户间转账操作

需求微缩：A账户减钱，B账户加钱

分析:

数据层提供基础操作，指定账户减钱（outMoney），指定账户加钱（inMoney）

业务层提供转账操作（transfer），调用减钱与加钱操作

提供2个账户和操作金额执行转账操作

基于Spring整合MyBatis环境搭建上述操作

结果分析：

程序正常执行时，账户金额A减B加没有问题

程序出现异常后，转账失败，但是异常之后操作失败，整体业务失败

1.      public void transfer(String out,String in ,Double money) {
2.          accountDao.outMoney(out,money);
3.  int i = 1/0;
4.          accountDao.inMoney(in,money);
5.      }

- 在需要添加事务的接口上添加Spring事务管理

1.  public interface AccountService {
2.      _/\*\*_
3.       \* 转账操作
4.       \* @param out 传出方
5.       \* @param in 转入方
6.       \* @param money 金额
7.       \*/
8.      _//配置当前接口方法具有事务_
9.      @Transactional
10.     public void transfer(String out,String in ,Double money) ;
11. }

Spring注解式事务通常添加在业务层接口中，降低耦合

注解式事务可以添加到业务方法上表示当前方法开启事务，也可以添加到接口上表示当前接口所有方法开启事务

- 设置事务管理器

JdbcConfig

1.      _//配置事务管理器，mybatis使用的是jdbc事务_
2.      @Bean
3.      public PlatformTransactionManager transactionManager(DataSource dataSource){
4.          DataSourceTransactionManager transactionManager = new DataSourceTransactionManager();
5.          transactionManager.setDataSource(dataSource);
6.          return transactionManager;
7.      }

- 开启注解式事务驱动

SpringConfig

1.  @Configuration
2.  @ComponentScan("com.itheima")
3.  @PropertySource("classpath:jdbc.properties")
4.  @Import({JdbcConfig.class,MybatisConfig.class})
5.  _//开启注解式事务驱动_
6.  @EnableTransactionManagement
7.  public class SpringConfig {
8.  }

##### Spring事务角色

事务1（事务协调员）

|

1.      @Update("update tbl_account set money = money + #{money} where name = #{name}")
2.      void inMoney(@Param("name") String name, @Param("money") Double money);

3.      @Update("update tbl_account set money = money - #{money} where name = #{name}")
4.      void outMoney(@Param("name") String name, @Param("money") Double money);

|

事务2（事务协调员）

1.      public void transfer(String out,String in ,Double money) {
2.          accountDao.outMoney(out,money);
3.          accountDao.inMoney(in,money);
4.      }

|

事务3（事务管理员）

Spring将事务1 2全部加入事务3中，只剩1个事务

事务管理员：发起事务方，在Spring中通常指业务层开启事务的方法

事务协调员：加入事务方，在Spring中通常指数据层方法，也可以是业务层方法

##### Spring事务属性

1.  事务配置

@Transactional(rollbackFor = IOException.class)

设置回滚异常（class）

readOnly 设置只读事务 readOnly = true 只读事务

timeout 设置事务超时时间 timeout = -1 永不超时

rollbackFor 设置回滚异常（class）

rollbackForClassName设置回滚异常（String）

noRollbackFor 设置事务不回滚异常（class）

noRollbackForClassName 设置事务不回滚异常（String）

propagation 设置事务传播行为

1.  案例：转账业务追加日志

需求：实现任意两个账户转账操作，并对每次转账操作在数据库留痕

需求微缩：A账户减钱，B账户加钱，数据库记录日志

分析：

基于转账操作案例添加日志模块，实现数据库中记录日志

业务层转账操作（transfer）调用减钱，加钱，与记录日志功能

实现效果预期：

不论转账操作是否成功，均记录留痕

问题：

日志的记录与转账操作隶属于同一个事务，同成功同失败

1.      public void transfer(String out,String in ,Double money) {
2.          try{
3.              accountDao.outMoney(out,money);
4.              int i = 1/0;
5.              accountDao.inMoney(in,money);
6.          }finally {
7.              logService.log(out,in,money);
8.          }
9.      }

对应三个事务，log与update1与update2 同时隶属于这个Spring事务

要求log不要加入事务

1.  事务传播行为

事务协调员对事务管理员所携带事务的处理态度

propagation 设置事务传播行为

1.  public interface LogService {
2.      _//propagation设置事务属性：传播行为设置为当前操作需要新事务_
3.      @Transactional(propagation = Propagation.REQUIRES_NEW)
4.      void log(String out, String in, Double money);
5.  }

设置事务传播行为REQUIRES_NEW 需要新事务

|     |     |     |
| --- | --- | --- |
| 传播属性 | 事务管理员 | 事务协调员 |
| REQUIRED（默认） | 开启T | 加入T |
| 无   | 新建T2 |
| REQUIRED_NEW | 开启T | 新建T2 |
| 无   | 新建T2 |
| SUPPORTS | 开启T | 加入T |
| 无   | 无   |
| NOT_SUPPORTED | 开启T | 无   |
| 无   | 无   |
| MANDATORY | 开启T | 加入T |
| 无   | ERROR |
| NEVER | 开启T | ERROR |
| 无   | 无   |
| NSESTED | 设置savePoint，一旦事务回滚，事务将回滚到savePoint处，交由客户响应提交/回滚 |     |

## SpringMVC

SpringMVC技术与Servlet技术功能等同，均属于web（表现层）层开发技术

### SpringMVC简介

@ResponseBody注解用于将控制器方法返回的对象转换为JSON或XML数据并直接写入HTTP响应体，常用于异步请求处理。@RequestBody则用于从前端请求中读取JSON或XML数据，并将其绑定到方法参数上。

页面————后端服务器

HTML 表现层（此前使用Servlet，现在使用SpringMVC替代）

CSS 业务层

VUE 数据层（Mybatis）

ElementUI

SpringMVC是一种基于Java实现MVC模型的轻量级Web框架

优点：使用简单，开发便捷，灵活性强

#### SpringMVC入门案例

1.  使用SpringMVC技术需要先导入SpringMVC与Servlet坐标
2.      <dependency>
3.        <groupId>javax.servlet</groupId>
4.        <artifactId>javax.servlet-api</artifactId>
5.        <version>3.1.0</version>
6.        <scope>provided</scope>ws
7.      </dependency>
8.      <dependency>
9.        <groupId>org.springframework</groupId>
10.       <artifactId>spring-webmvc</artifactId>
11.       <version>5.2.10.RELEASE</version>
12.     </dependency>

13.  创建SpringMVC控制器类（同Servlet）
14.  _//定义表现层控制器bean_
15.  @Controller
16.  public class UserController {

17.      _//设置映射路径为/save，即外部访问路径_
18.      @RequestMapping("/save")
19.      _//设置当前操作返回结果为指定json数据（本质上是一个字符串信息）_
20.      @ResponseBody
21.     public String save(){
22.         System.out.println("user save ...");
23.         return "{'info':'springmvc'}";
24.     }

25.     _//设置映射路径为/delete，即外部访问路径_
26.     @RequestMapping("/delete")
27.     @ResponseBody
28.     public String delete(){
29.         System.out.println("user save ...");
30.         return "{'info':'springmvc'}";
31.     }
32. }

33.  初始化SpringMVC环境（同Spring环境），设定SpringMVC加载Controller对应的bean
34.  _//springmvc配置类，本质上还是一个spring配置类_
35.  @Configuration
36.  @ComponentScan("com.itheima.controller")
37.  public class SpringMvcConfig {
38.  }

39.  初始化Servlet容器（Tomcat），加载SpringMVC环境并设置SpringMVC技术处理的请求
40.  _//web容器配置类_
41.  public class ServletContainersInitConfig extends AbstractDispatcherServletInitializer {
42.      _//加载springmvc配置类，产生springmvc容器（本质还是spring容器）_
43.      protected WebApplicationContext createServletApplicationContext() {
44.          _//初始化WebApplicationContext对象_
45.          AnnotationConfigWebApplicationContext ctx = new AnnotationConfigWebApplicationContext();
46.          _//加载指定配置类_
47.          ctx.register(SpringMvcConfig.class);
48.         return ctx;
49.     }

50.     _//设置由springmvc控制器处理的请求映射路径 哪些请求归属SpringMVC处理_
51.     protected String\[\] getServletMappings() {
52.         return new String\[\]{"/"};
53.     }

54.     _//加载spring配置类_
55.     protected WebApplicationContext createRootApplicationContext() {
56.         return null;
57.     }
58. }

@Controller

类注解

SpringMVC控制器定义上方

设定SpringMVC的核心控制器bean

@ResponseBody

方法注解

SpringMVC控制器方法定义上方

设置当前控制器方法响应内容为当前返回值，无需解析

SpringMVC开发总结（1+N）

- 一次性工作

创建工程，设置服务器，加载工程

导入坐标

创建Web容器启动类，加载SpringMVC配置，并设置SpringMVC请求拦截路径

SpringMVC核心配置类（设置配置类，扫描Controller包，加载Controller控制器bean）

- 多次工作

定义处理请求的控制器类

定义处理请求方法，并配置映射路径（@RequestMapping）与返回json数据（@ResponseBody）

#### 入门案例工作流程

启动服务器初始化过程：

1.  服务器启动，执行ServletContainerInitConfig类，初始化web容器
2.  执行createServletAplicationContext方法，创建WebApplicationContext对象
3.  加载SpringMvcConfig
4.  执行@ConponentScan加载对应的bean
5.  加载UserController，每个@RequestMapping的名称对应一个具体方法
6.  执行getServletMappings方法，定义所有的请求都通过SpringMVC

单次请求过程

1.  发送请求localhost/save
2.  Web容器发现所有请求都经过SpringMVC，将请求交给SpringMVC处理
3.  解析请求路径/save
4.  由/save匹配执行对应的方法save（）
5.  执行save（）
6.  检测到@ResponseBody直接将save（）方法的返回值作为响应请求体返回给请求方

#### Bean加载控制

因为功能不同，怎么避免Spring错误地加载到Controller（SpringMVC）的bean

\--加载Spring控制的bean的时候，排除掉SpringMVC控制的bean

两种方式：扫描指定包/过滤

1.  @Configuration
2.  _//@ComponentScan({"com.itheima.service","com.itheima.dao"})_

3.  _//设置spring配置类加载bean时的过滤规则，当前要求排除掉表现层对应的bean_
4.  _//excludeFilters属性：设置扫描加载bean时，排除的过滤规则_
5.  _//type属性：设置排除规则，当前使用按照bean定义时的注解类型进行排除_
6.  _//classes属性：设置排除的具体注解类，当前设置排除@Controller定义的bean_
7.  @ComponentScan(value="com.itheima",
8.      excludeFilters = @ComponentScan.Filter(
9.         type = FilterType.ANNOTATION,
10.         classes = Controller.class
11.     )
12. )
13. public class SpringConfig {
14. }

ANNOTATION//按照注解过滤

ASSIGNABLE_TYPE //按照类型过滤

ASPECTJ//按照ASPECTJ表达式过滤

REGEX//按照正则表达式过滤

CUSTOM//按照自定义的过滤规则过滤

简化开发

1.  _//web配置类简化开发，仅设置配置类类名即可_
2.  public class ServletContainersInitConfig extends AbstractAnnotationConfigDispatcherServletInitializer {

3.      protected Class<?>\[\] getRootConfigClasses() {
4.          return new Class\[\]{SpringConfig.class};
5.      }

6.      protected Class<?>\[\] getServletConfigClasses() {
7.          return new Class\[\]{SpringMvcConfig.class};
8.     }

9.     protected String\[\] getServletMappings() {
10.         return new String\[\]{"/"};
11.     }
12. }

修改继承的类，简化配置

#### PostMan

功能强大的网页调试与发送网页HTTP请求的Chrome插件

作用：常用于接口测试

### 请求与响应

#### 请求映射路径

团队多人开发，每人设置不同的请求路径，冲突问题解决——设置模块名作为请求路径前缀

1.  @Controller
2.  _//类上方配置的请求映射与方法上面配置的请求映射连接在一起，形成完整的请求映射路径_
3.  @RequestMapping("/user")
4.  public class UserController {
5.      _//请求路径映射_
6.      @RequestMapping("/save")
7.      @ResponseBody
8.      public String save(){
9.          System.out.println("user save ...");
10.         return "{'module':'user save'}";
11.     }
12. }

@RequestMapping

方法注解/类注解

类上方配置的请求映射与方法上面配置的请求映射连接在一起，形成完整的请求映射路径

#### 请求参数

##### 普通参数传递

请求参数与形参名称相同

1.  _//普通参数：请求参数与形参名称对应即可完成参数传递_
2.      @RequestMapping("/commonParam")
3.      @ResponseBody
4.      public String commonParam(String name ,int age){
5.          System.out.println("普通参数传递 name ==> "+name);
6.          System.out.println("普通参数传递 age ==> "+age);
7.          return "{'module':'common param'}";
8.      }

请求参数与形参名称不同

1.      _//普通参数：请求参数名与形参名不同时，使用@RequestParam注解关联请求参数名称与形参名称之间的关系_
2.      @RequestMapping("/commonParamDifferentName")
3.      @ResponseBody
4.      public String commonParamDifferentName(@RequestParam("name") String userName , int age){
5.          System.out.println("普通参数传递 userName ==> "+userName);
6.          System.out.println("普通参数传递 age ==> "+age);
7.          return "{'module':'common param different name'}";
8.      }

@RequestParam("name") String userName使用这个来绑定请求参数与形参

GET请求传参

普通参数：

url地址传参，地址参数名与形参变量名相同，定义形参即可接受参数

POST请求

普通参数：

form表单post请求传参，表单参数名与形参变量名相同，定义形参即可接受参数

Postman页

Post请求中输入中文出现乱码处理

ServletContainerInitConfig

1.      _//乱码处理_
2.      @Override
3.      protected Filter\[\] getServletFilters() {
4.          CharacterEncodingFilter filter = new CharacterEncodingFilter();
5.          filter.setEncoding("UTF-8");
6.          return new Filter\[\]{filter};
7.      }

##### 其余四种参数传递

1.  POJO传参

请求参数与形参对象属性名相同，定义POJO类型形参即可接受参数

1.  public class User {
2.      private String name;
3.      private int age;
4.      private Address address;
5.  ...
6.  }

请求参数与形参对象中属性对应

1.  _//POJO参数：请求参数与形参对象中的属性对应即可完成参数传递_
2.      @RequestMapping("/pojoParam")
3.      @ResponseBody
4.      public String pojoParam(User user){
5.          System.out.println("pojo参数传递 user ==> "+user);
6.          return "{'module':'pojo param'}";
7.      }
8.  嵌套POJO传参

POJO中包含POJO对象

1.      _//嵌套POJO参数：嵌套属性按照层次结构设定名称即可完成参数传递_
2.      @RequestMapping("/pojoContainPojoParam")
3.      @ResponseBody
4.      public String pojoContainPojoParam(User user){
5.          System.out.println("pojo嵌套pojo参数传递 user ==> "+user);
6.          return "{'module':'pojo contain pojo param'}";
7.      }
8.  数组传参
9.      _//数组参数：同名请求参数可以直接映射到对应名称的形参数组对象中_
10.     @RequestMapping("/arrayParam")
11.     @ResponseBody
12.     public String arrayParam(String\[\] likes){
13.         System.out.println("数组传递 likes ==> "+ Arrays.toString(likes));
14.         return "{'module':'array param'}";
15.     }
16. 集合传参
17.     _//集合参数：同名请求参数可以使用@RequestParam注解映射到对应名称的集合对象中作为数据_
18.     @RequestMapping("/listParam")
19.     @ResponseBody
20.     public String listParam(@RequestParam List<String> likes){
21.         System.out.println("集合参数传递 likes ==> "+ likes);
22.         return "{'module':'list param'}";
23.     }

##### json数据传递参数（接收请求中的json数据）

Step1：导入json依赖

1.      <dependency>
2.        <groupId>com.fasterxml.jackson.core</groupId>
3.        <artifactId>jackson-databind</artifactId>
4.        <version>2.9.0</version>
5.      </dependency>

Step1.5：Postman设置发json数据

Step2：开启由json对象转换为对象功能

1.  @Configuration
2.  @ComponentScan("com.itheima.controller")
3.  _//开启json数据类型自动转换_
4.  @EnableWebMvc
5.  public class SpringMvcConfig {
6.  }

Step3：设置接收json数据

集合参数：json格式

1.      _//集合参数：json格式_
2.      _//1.开启json数据格式的自动转换，在配置类中开启@EnableWebMvc_
3.      _//2.使用@RequestBody注解将外部传递的json数组数据映射到形参的保存实体类对象的集合对象中，要求属性名称一一对应_
4.      @RequestMapping("/listPojoParamForJson")
5.      @ResponseBody
6.      public String listPojoParamForJson(@RequestBody List<User> likes){
7.          System.out.println("list pojo(json)参数传递 list ==> "+likes);
8.          return "{'module':'list pojo for json param'}";
9.      }

Json现在不在requestParam中了，在请求体中

Pojo参数：json格式

1.      _//POJO参数：json格式_
2.      _//1.开启json数据格式的自动转换，在配置类中开启@EnableWebMvc_
3.      _//2.使用@RequestBody注解将外部传递的json数据映射到形参的实体类对象中，要求属性名称一一对应_
4.      @RequestMapping("/pojoParamForJson")
5.      @ResponseBody
6.      public String pojoParamForJson(@RequestBody User user){
7.          System.out.println("pojo(json)参数传递 user ==> "+user);
8.          return "{'module':'pojo for json param'}";
9.      }

Pojo参数：json数组

1.      _//集合参数：json格式_
2.      _//1.开启json数据格式的自动转换，在配置类中开启@EnableWebMvc_
3.      _//2.使用@RequestBody注解将外部传递的json数组数据映射到形参的保存实体类对象的集合对象中，要求属性名称一一对应_
4.      @RequestMapping("/listPojoParamForJson")
5.      @ResponseBody
6.      public String listPojoParamForJson(@RequestBody List<User> list){
7.          System.out.println("list pojo(json)参数传递 list ==> "+list);
8.          return "{'module':'list pojo for json param'}";
9.      }

后期开发中，发送json格式数据为主，@RequestBody应用较广

如果发送非json格式数据，选用@RequestParam接收请求参数

##### 日期类型参数传递

1.      _//日期参数_
2.      _//使用@DateTimeFormat注解设置日期类型数据格式，默认格式yyyy/MM/dd_
3.      @RequestMapping("/dataParam")
4.      @ResponseBody
5.      public String dataParam(Date date,
6.                              @DateTimeFormat(pattern="yyyy-MM-dd") Date date1,
7.                              @DateTimeFormat(pattern="yyyy/MM/dd HH:mm:ss") Date date2）{
8.          System.out.println("参数传递 date ==> "+date);
9.          System.out.println("参数传递 date1(yyyy-MM-dd) ==> "+date1);
10.         System.out.println("参数传递 date2(yyyy/MM/dd HH:mm:ss) ==> "+date2);
11.         return "{'module':'data param'}";
12.     }

底层逻辑实现：Converter接口

@EnableWebMvc功能之一：根据类型匹配对应的类型转换器

#### 响应

##### 响应页面/文本数据

1.  _//响应页面/跳转页面_
2.      _//返回值为String类型，设置返回值为页面名称，即可实现页面跳转_
3.      @RequestMapping("/toJumpPage")
4.      public String toJumpPage(){
5.          System.out.println("跳转页面");
6.          return "page.jsp";
7.      }

8.      _//响应文本数据_
9.     _//返回值为String类型，设置返回值为任意字符串信息，即可实现返回指定字符串信息，需要依赖@ResponseBody注解_
10.     @RequestMapping("/toText")
11.     @ResponseBody
12.     public String toText(){
13.         System.out.println("返回纯文本数据");
14.         return "response text";
15.     }

16.  响应pojo对象
17.      _//响应POJO对象_
18.      _//返回值为实体类对象，设置返回值为实体类类型，即可实现返回对应对象的json数据，需要依赖@ResponseBody注解和@EnableWebMvc注解_
19.      @RequestMapping("/toJsonPOJO")
20.      @ResponseBody
21.      public User toJsonPOJO(){
22.          System.out.println("返回json对象数据");
23.          User user = new User();
24.          user.setName("itcast");
25.         user.setAge(15);
26.         return user;
27.     }

@ResponseBody

类型：方法注解

位置：SpringMVC控制器定义上方

作用：设置当前控制器返回值作为响应体

通过HttpMessageConverter接口（类型转换器）实现

### REST风格

#### REST简介

Representational State Transfer 表现形式状态转换

- 传统风格资源描述形式：

http://localhost/user/getById?id=1

http://localhost/user/saveUser

REST风格描述形式：

http://localhost/user/1

http://localhost/user

- 优点：

隐藏资源的访问行为，无法通过地址得知对资源是何种操作

书写简化

- 按照REST风格访问资源时使用行为动作区分你对资源进行了何种操作

http://localhost/user 查询全部用户信息 GET（查询）

http://localhost/user/1 查询指定用户信息 GET（查询）

http://localhost/user 添加用户信息 POST（新增/保存）

http://localhost/user 修改用户信息 PUT（修改/更新）

http://localhost/user/1 删除用户信息 DELETE（删除）

上述行为是约定行为，约定不是规范，可以打破，所以成为REST风格，而不是规范

描述模块的名称通常使用复数，也就是加s的格式描述，表示此类资源，而非单个资源

根据REST风格对资源进行访问成为RESTful

#### RESTful入门案例

保存

1.      _//设置当前请求方法为POST，表示REST风格中的添加操作_
2.      @RequestMapping(value = "/users",method = RequestMethod.POST)
3.      @ResponseBody
4.      public String save(){
5.          System.out.println("user save...");
6.          return "{'module':'user save'}";
7.      }    

使用method配置

删除

1.  _//设置当前请求方法为DELETE，表示REST风格中的删除操作_
2.      _//@PathVariable注解用于设置路径变量（路径参数），要求路径上设置对应的占位符，并且占位符名称与方法形参名称相同_
3.      @RequestMapping(value = "/users/{id}",method = RequestMethod.DELETE)
4.      @ResponseBody
5.      public String delete(@PathVariable Integer id){
6.          System.out.println("user delete..." + id);
7.          return "{'module':'user delete'}";
8.      }

更新

1.  _//设置当前请求方法为PUT，表示REST风格中的修改操作_
2.      @RequestMapping(value = "/users",method = RequestMethod.PUT)
3.      @ResponseBody
4.      public String update(@RequestBody User user){
5.          System.out.println("user update..."+user);
6.          return "{'module':'user update'}";
7.      }

查询指定

1.   _//设置当前请求方法为GET，表示REST风格中的查询操作_
2.      _//@PathVariable注解用于设置路径变量（路径参数），要求路径上设置对应的占位符，并且占位符名称与方法形参名称相同_
3.      @RequestMapping(value = "/users/{id}" ,method = RequestMethod.GET)
4.      @ResponseBody
5.      public String getById(@PathVariable Integer id){
6.          System.out.println("user getById..."+id);
7.          return "{'module':'user getById'}";
8.      }

查询全部

1.      _//设置当前请求方法为GET，表示REST风格中的查询操作_
2.      @RequestMapping(value = "/users",method = RequestMethod.GET)
3.      @ResponseBody
4.      public String getAll(){
5.          System.out.println("user getAll...");
6.          return "{'module':'user getAll'}";
7.      }

流程：

设定http请求动作

设定请求参数（路径变量）@PathVariable

@RequestParam用于接收url地址传参或表单传参

@RequestBody用于接收json数据

@PathVariable用于接收路径参数，使用{参数名称}描述路径参数

在开发中，发送请求参数超过1个时，以json格式为主，@RequestBody应用较广，当参数数量较少时，可以采用@PathVariable接受请求路径变量，通常用于传递id值，通常偏向于将多个需要提交的数据封装成pojo，然后通过json串的形式传递

#### REST快速开发（简化开发）

1.  _//@Controller_
2.  _//@ResponseBody配置在类上可以简化配置，表示设置当前每个方法的返回值都作为响应体_
3.  _//@ResponseBody_
4.  @RestController     
5.  _//使用@RestController注解替换@Controller与@ResponseBody注解，简化书写_
6.  @RequestMapping("/books")
7.  public class BookController {

8.  _//    @RequestMapping( method = RequestMethod.POST)_
9.     @PostMapping        
10. _//使用@PostMapping简化Post请求方法对应的映射配置_
11.     public String save(@RequestBody Book book){
12.         System.out.println("book save..." + book);
13.         return "{'module':'book save'}";
14.     }

15. _//    @RequestMapping(value = "/{id}" ,method = RequestMethod.DELETE)_
16.     @DeleteMapping("/{id}")     
17. _//使用@DeleteMapping简化DELETE请求方法对应的映射配置_
18.     public String delete(@PathVariable Integer id){
19.         System.out.println("book delete..." + id);
20.         return "{'module':'book delete'}";
21.     }

22. _//    @RequestMapping(method = RequestMethod.PUT)_
23.     @PutMapping         
24. _//使用@PutMapping简化Put请求方法对应的映射配置_
25.     public String update(@RequestBody Book book){
26.         System.out.println("book update..."+book);
27.         return "{'module':'book update'}";
28.     }

29. _//    @RequestMapping(value = "/{id}" ,method = RequestMethod.GET)_
30.     @GetMapping("/{id}")    
31. _//使用@GetMapping简化GET请求方法对应的映射配置_
32.     public String getById(@PathVariable Integer id){
33.         System.out.println("book getById..."+id);
34.         return "{'module':'book getById'}";
35.     }

36. _//    @RequestMapping(method = RequestMethod.GET)_
37.     @GetMapping             
38. _//使用@GetMapping简化GET请求方法对应的映射配置_
39.     public String getAll(){
40.         System.out.println("book getAll...");
41.         return "{'module':'book getAll'}";
42.     }
43. }

@RestController替换@Controller与@ResponseBody注解，简化书写

@GetMapping @PostMapping @PutMapping @DeleteMapping 每个都对应一个请求动作

#### 案例：基于RESTful页面数据交互

接口制作

1.  @RestController
2.  @RequestMapping("/books")
3.  public class BookController {

4.      @PostMapping
5.      public String save(@RequestBody Book book){
6.          System.out.println("book save ==> "+ book);
7.          return "{'module':'book save success'}";
8.      }

9.     @GetMapping
10.     public List<Book> getAll(){ 
11.         System.out.println("book getAll is running ...");
12.         List<Book> bookList = new ArrayList<Book>();

13.         Book book1 = new Book();
14.         book1.setType("计算机");
15.         book1.setName("SpringMVC入门教程");
16.         book1.setDescription("小试牛刀");
17.         bookList.add(book1);

18.         Book book2 = new Book();
19.         book2.setType("计算机");
20.         book2.setName("SpringMVC实战教程");
21.         book2.setDescription("一代宗师");
22.         bookList.add(book2);

23.         Book book3 = new Book();
24.         book3.setType("计算机丛书");
25.         book3.setName("SpringMVC实战教程进阶");
26.         book3.setDescription("一代宗师呕心创作");
27.         bookList.add(book3);

28.         return bookList;
29.     }

30. }

与前端页面结合

发现localhost/book.html不能跑通，问题出现在getServletMappings中，对于静态资源的访问不需要过SpringMVC

1.  protected String\[\] getServletMappings() {
2.          return new String\[\]{"/"};
3.      }

新建一个SpringMvcSupport配置

1.  @Configuration
2.  public class SpringMvcSupport extends WebMvcConfigurationSupport {
3.      _//设置静态资源访问过滤，当前类需要设置为配置类，并被扫描加载_
4.      @Override
5.      protected void addResourceHandlers(ResourceHandlerRegistry registry) {
6.          _//当访问/pages/????时候，从/pages目录下查找内容_
7.          registry.addResourceHandler("/pages/\*\*").addResourceLocations("/pages/");
8.          registry.addResourceHandler("/js/\*\*").addResourceLocations("/js/");
9.          registry.addResourceHandler("/css/\*\*").addResourceLocations("/css/");
10.         registry.addResourceHandler("/plugins/\*\*").addResourceLocations("/plugins/");
11.     }
12. }

加入扫包

1.  @Configuration
2.  @ComponentScan({"com.itheima.controller","com.itheima.config"})
3.  @EnableWebMvc
4.  public class SpringMvcConfig {
5.  }

前端页面设计省略，axios发送异步请求

并在前端页面上绑定按钮

1.  <script>
2.          var vue = new Vue({

3.              el: '#app',

4.              data:{
5.      dataList: \[\],_//当前页要展示的分页列表数据_
6.                  formData: {},_//表单数据_
7.                  dialogFormVisible: false,_//增加表单是否可见_
8.                 dialogFormVisible4Edit:false,_//编辑表单是否可见_
9.                 pagination: {},_//分页模型数据，暂时弃用_
10.             },

11.             _//钩子函数，VUE对象初始化完成后自动执行_
12.             created() {
13.                 this.getAll();
14.             },

15.             methods: {
16.                 _// 重置表单_
17.                 resetForm() {
18.                     _//清空输入框_
19.                     this.formData = {};
20.                 },

21.                 _// 弹出添加窗口_
22.                 openSave() {
23.                     this.dialogFormVisible = true;
24.                     this.resetForm();
25.                 },

26.                 _//添加_
27.                 saveBook () {
28.                     axios.post("/books",this.formData).then((res)=>{

29.                     });
30.                 },

31.                 _//主页列表查询_
32.                 getAll() {
33.                     axios.get("/books").then((res)=>{
34.                         this.dataList = res.data;
35.                     });
36.                 },

37.             }
38.         })
39.     </script>

小结：

制作SpringMVC控制器，并通过PostMan测试接口功能（使用假数据）

设置对静态资源的访问放行

前端页面通过异步提交访问后台控制器

### SSM整合

#### SSM整合

SSM整合流程

1.  创建工程
2.  SSM整合

- Spring
- SpringConfig
- MyBatis
- MyBatisConfig
- jdbcConfig
- jdbc.properties
- SpringMVC
- ServletConfig
- SpringMvcConfig

1.  功能模块

- 表与实体类
- Dao（接口+自动代理）
- Service（接口+实现类）
- 业务层接口测试（整合JUnit）
- Controller
- 表现层接口测试（Postman）

##### 创建工程

需要导入坐标

Spring-webmvc/Spring-jdbc/Spring-test/Mybatis/Mysql/Druid/Junit/Servlet/Jackson

##### SSM整合配置

SpringConfig

1.  @Configuration
2.  @ComponentScan({"com.itheima.service"})
3.  @PropertySource("classpath:jdbc.properties")
4.  @Import({JdbcConfig.class,MyBatisConfig.class})
5.  @EnableTransactionManagement
6.  public class SpringConfig {
7.  }

加载jdbc.properties

再加载jdbcConfig与MyBatisConfig

JdbcConfig

1.  public class JdbcConfig {
2.      @Value("${jdbc.driver}")
3.      private String driver;
4.      @Value("${jdbc.url}")
5.      private String url;
6.      @Value("${jdbc.username}")
7.      private String username;
8.      @Value("${jdbc.password}")
9.      private String password;

10.     @Bean
11.     public DataSource dataSource(){
12.         DruidDataSource dataSource = new DruidDataSource();
13.         dataSource.setDriverClassName(driver);
14.         dataSource.setUrl(url);
15.         dataSource.setUsername(username);
16.         dataSource.setPassword(password);
17.         return dataSource;
18.     }

19.     @Bean
20.     public PlatformTransactionManager transactionManager(DataSource dataSource){
21.         DataSourceTransactionManager ds = new DataSourceTransactionManager();
22.         ds.setDataSource(dataSource);
23.         return ds;
24.     }
25. }

MyBatisConfig

1.  public class MyBatisConfig {
2.      @Bean
3.      public SqlSessionFactoryBean sqlSessionFactory(DataSource dataSource){
4.          SqlSessionFactoryBean factoryBean = new SqlSessionFactoryBean();
5.          factoryBean.setDataSource(dataSource);
6.          factoryBean.setTypeAliasesPackage("com.itheima.domain");
7.          return factoryBean;
8.      }
9.  }

SpringMvcConfig

1.  @Configuration
2.  @ComponentScan("com.itheima.controller")
3.  @EnableWebMvc
4.  public class SpringMvcConfig {
5.  }

ServletConfig

1.  public class ServletConfig extends AbstractAnnotationConfigDispatcherServletInitializer {
2.      protected Class<?>\[\] getRootConfigClasses() {
3.          return new Class\[\]{SpringConfig.class};
4.      }

5.      protected Class<?>\[\] getServletConfigClasses() {
6.          return new Class\[\]{SpringMvcConfig.class};
7.      }

8.     protected String\[\] getServletMappings() {
9.         return new String\[\]{"/"};
10.     }
11. }

还可以创建一个过滤器来处理中文表单提交乱码的过滤

##### 功能模块

创建实体类Book

1.  public class Book {
2.      private Integer id;
3.      private String type;
4.      private String name;
5.      private String description;

6.      @Override
7.      public String toString() {
8.          return "Book{" +
9.                 "id=" + id +
10.                 ", type='" + type + '\\'' +
11.                 ", name='" + name + '\\'' +
12.                 ", description='" + description + '\\'' +
13.                 '}';
14.     }

15.     public Integer getId() {
16.         return id;
17.     }

18.     public void setId(Integer id) {
19.         this.id = id;
20.     }

21.     public String getType() {
22.         return type;
23.     }

24.     public void setType(String type) {
25.         this.type = type;
26.     }

27.     public String getName() {
28.         return name;
29.     }

30.     public void setName(String name) {
31.         this.name = name;
32.     }

33.     public String getDescription() {
34.         return description;
35.     }

36.     public void setDescription(String description) {
37.         this.description = description;
38.     }
39. }

BookDao

1.  public interface BookDao {

2.  //    @Insert("insert into tbl_book values(null,#{type},#{name},#{description})")
3.      @Insert("insert into tbl_book (type,name,description) values(#{type},#{name},#{description})")
4.      public void save(Book book);

5.      @Update("update tbl_book set type = #{type}, name = #{name}, description = #{description} where id = #{id}")
6.      public void update(Book book);

7.     @Delete("delete from tbl_book where id = #{id}")
8.     public void delete(Integer id);

9.     @Select("select \* from tbl_book where id = #{id}")
10.     public Book getById(Integer id);

11.     @Select("select \* from tbl_book")
12.     public List<Book> getAll();
13. }

BookService

1.  public interface BookService {

2.      _/\*\*_
3.       \* 保存
4.       \* @param book
5.       \* @return
6.       \*/
7.      public boolean save(Book book);

8.     _/\*\*_
9.      \* 修改
10.      \* @param book
11.      \* @return
12.      \*/
13.     public boolean update(Book book);

14.     _/\*\*_
15.      \* 按id删除
16.      \* @param id
17.      \* @return
18.      \*/
19.     public boolean delete(Integer id);

20.     _/\*\*_
21.      \* 按id查询
22.      \* @param id
23.      \* @return
24.      \*/
25.     public Book getById(Integer id);

26.     _/\*\*_
27.      \* 查询全部
28.      \* @return
29.      \*/
30.     public List<Book> getAll();
31. }

BookServiceImpl

1.  @Service
2.  public class BookServiceImpl implements BookService {
3.      @Autowired
4.      private BookDao bookDao;

5.      public boolean save(Book book) {
6.          bookDao.save(book);
7.          return true;
8.      }

9.     public boolean update(Book book) {
10.         bookDao.update(book);
11.         return true;
12.     }

13.     public boolean delete(Integer id) {
14.         bookDao.delete(id);
15.         return true;
16.     }

17.     public Book getById(Integer id) {
18.         return bookDao.getById(id);
19.     }

20.     public List<Book> getAll() {
21.         return bookDao.getAll();
22.     }
23. }

出现bookDao爆红，是因为Spring中没有配bookDao的bean，使用的是mybatis自动代理，所以就没有对应的bean自动装配，但是这里不会影响程序的正常运行

可行的解决方案：

使用构造器注入或者直接忽略错误因为不会影响运行

BookController

1.  @RestController
2.  @RequestMapping("/books")
3.  public class BookController {

4.      @Autowired
5.      private BookService bookService;

6.      @PostMapping
7.      public boolean save(@RequestBody Book book) {
8.         return bookService.save(book);
9.     }

10.     @PutMapping
11.     public boolean update(@RequestBody Book book) {
12.         return bookService.update(book);
13.     }

14.     @DeleteMapping("/{id}")
15.     public boolean delete(@PathVariable Integer id) {
16.         return bookService.delete(id);
17.     }

18.     @GetMapping("/{id}")
19.     public Book getById(@PathVariable Integer id) {
20.         return bookService.getById(id);
21.     }

22.     @GetMapping
23.     public List<Book> getAll() {
24.         return bookService.getAll();
25.     }
26. }

使用RequestMapping配置公共映射

然后使用REST风格

##### 测试

业务层接口测试（整合JUnit）/表现层接口测试（Postman）

业务层（Service）测试

1.  @RunWith(SpringJUnit4ClassRunner.class)
2.  @ContextConfiguration(classes = SpringConfig.class)
3.  public class BookServiceTest {

4.      @Autowired
5.      private BookService bookService;

6.      @Test
7.      public void testGetById(){
8.         Book book = bookService.getById(1);
9.         System.out.println(book);
10.     }

11.     @Test
12.     public void testGetAll(){
13.         List<Book> all = bookService.getAll();
14.         System.out.println(all);
15.     }

16. }

表现层测试（Postman）

##### 添加事务管理

在SpringConfig中使用@EnableTransactionManagement开启事务管理

JdbcConfig

1.      @Bean
2.      public PlatformTransactionManager transactionManager(DataSource dataSource){
3.          DataSourceTransactionManager ds = new DataSourceTransactionManager();
4.          ds.setDataSource(dataSource);
5.          return ds;
6.      }

BookService

1.  @Transactional

挂上事务，先不配事务

#### 表现层数据封装（前后端数据协议）

前端接收数据格式

\-创建结果模型类，封装到data属性中

\-封装特殊信息到message（msg）属性中

Controller-result

1.  public class Result {
2.      _//描述统一格式中的数据_
3.      private Object data;
4.      _//描述统一格式中的编码，用于区分操作，可以简化配置0或1表示成功失败_
5.      private Integer code;
6.      _//描述统一格式中的消息，可选属性_
7.      private String msg;

8.      public Result() {}

9.     public Result(Integer code,Object data) {
10.         this.data = data;
11.         this.code = code;
12.     }

13.     public Result(Integer code, Object data, String msg) {
14.         this.data = data;
15.         this.code = code;
16.         this.msg = msg;
17.     }

18.     public Object getData() {return data;}

19.     public void setData(Object data) {this.data = data;}

20.     public Integer getCode() {return code;}

21.     public void setCode(Integer code) {this.code = code;}

22.     public String getMsg() {return msg;}

23.     public void setMsg(String msg) {this.msg = msg;}
24. }

Controller-Code

1.  _//状态码_
2.  public class Code {
3.      public static final Integer SAVE_OK = 20011;
4.      public static final Integer DELETE_OK = 20021;
5.      public static final Integer UPDATE_OK = 20031;
6.      public static final Integer GET_OK = 20041;

7.      public static final Integer SAVE_ERR = 20010;
8.      public static final Integer DELETE_ERR = 20020;
9.     public static final Integer UPDATE_ERR = 20030;
10.     public static final Integer GET_ERR = 20040;
11. }

BookController

1.      @PostMapping
2.      public Result save(@RequestBody Book book) {
3.          boolean flag = bookService.save(book);
4.          return new Result(flag ? Code.SAVE_OK:Code.SAVE_ERR,flag);
5.      }

三步运算判断，flag如果成功（true）返回save_ok，如果失败返回save_err

1.      @GetMapping("/{id}")
2.      public Result getById(@PathVariable Integer id) {
3.          Book book = bookService.getById(id);
4.          Integer code = book != null ? Code.GET_OK : Code.GET_ERR;
5.          String msg = book != null ? "" : "数据查询失败，请重试！";
6.          return new Result(code,book,msg);
7.      }

#### 异常处理器

程序开发过程中不可避免的会遇到异常现象

出现异常现象的常见位置与常见诱因：

框架内部抛出的异常：因使用不合规导致

数据层抛出的异常：因外部服务器故障导致（服务器访问超时）

业务层抛出的异常：因业务逻辑书写错误导致（遍历业务书写操作，导致索引异常）

表现层抛出的异常：因数据收集，校验等规则导致（不匹配的数据类型间导致异常）

工具类抛出的异常：因工具类书写不严谨不够健壮导致（必要释放的连接长期未释放）

各个层级均出现异常，异常处理代码书写在哪一层？

\-所有的异常均抛出表现层进行处理

表现层处理异常，每个方法单独书写，代码书写量巨大且意义不强，解决-AOP思想

集中的 统一的处理项目中出现的异常

Controller中创建ProjectExceptionAdvice

1.  @RestControllerAdvice
2.  public class ProjectExceptionAdvice {   
3.  @ExceptionHandler(Exception.class)
4.      public Result doOtherException(Exception ex){
5.          return new Result(555,null);
6.      }
7.  }

#### 项目异常处理方案

项目异常分类以及处理方案：

- 业务异常-发送对应消息传递给用户，提醒规范操作（businessExpection）
- 规范的用户行为产生的异常
- 不规范的用户行为操作产生的异常
- 系统异常（SystemExpection）

\-发送固定消息传递给用户，安抚用户

\-发送特定消息给运维人员，提醒维护

\-记录日志

- 项目运行过程中可预计无法避免的异常
- 其他异常-发送固定消息传递给用户，安抚用户
- 编程人员未预期到的异常

新建一个exception类存放自定义异常处理器

1.  _//自定义异常处理器，用于封装异常信息，对异常进行分类_
2.  public class BusinessException extends RuntimeException{
3.      private Integer code;

4.      public Integer getCode() {
5.          return code;
6.      }

7.      public void setCode(Integer code) {
8.         this.code = code;
9.     }

10.     public BusinessException(Integer code, String message) {
11.         super(message);
12.         this.code = code;
13.     }

14.     public BusinessException(Integer code, String message, Throwable cause) {
15.         super(message, cause);
16.         this.code = code;
17.     }

18. }

加一个编号用于异常识别

BookServiceImpl 模拟业务异常/系统异常

1.      public Book getById(Integer id) {
2.          _//模拟业务异常，包装成自定义异常_
3.          if(id == 1){
4.              throw new BusinessException(Code.BUSINESS_ERR,"请不要使用你的技术挑战我的耐性!");
5.          }
6.          _//模拟系统异常，将可能出现的异常进行包装，转换成自定义异常_
7.          try{
8.              int i = 1/0;
9.          }catch (Exception e){
10.             throw new SystemException(Code.SYSTEM_TIMEOUT_ERR,"服务器访问超时，请重试!",e);
11.         }
12.         return bookDao.getById(id);
13.     }

ProjectExpectionAdvice

拦截并处理异常

1.  @RestControllerAdvice
2.  public class ProjectExceptionAdvice {
3.      _//@ExceptionHandler用于设置当前处理器类对应的异常类型_
4.      @ExceptionHandler(SystemException.class)
5.      public Result doSystemException(SystemException ex){
6.          _//记录日志_
7.          _//发送消息给运维_
8.          _//发送邮件给开发人员,ex对象发送给开发人员_
9.          return new Result(ex.getCode(),null,ex.getMessage());
10.     }

11.     @ExceptionHandler(BusinessException.class)
12.     public Result doBusinessException(BusinessException ex){
13.         return new Result(ex.getCode(),null,ex.getMessage());
14.     }

15.     _//除了自定义的异常处理器，保留对Exception类型的异常处理，用于处理非预期的异常_
16.     @ExceptionHandler(Exception.class)
17.     public Result doOtherException(Exception ex){
18.         _//记录日志_
19.         _//发送消息给运维_
20.         _//发送邮件给开发人员,ex对象发送给开发人员_
21.         return new Result(Code.SYSTEM_UNKNOW_ERR,null,"系统繁忙，请稍后再试！");
22.     }
23. }

#### 案例：SSM整合前台标准开发

前面已经完成了所有的后台，现在需要完成前台页面与后台的调通

SpringMvcSupport

设置对前端页面的放行

1.  @Configuration
2.  public class SpringMvcSupport extends WebMvcConfigurationSupport {
3.      @Override
4.      protected void addResourceHandlers(ResourceHandlerRegistry registry) {
5.          registry.addResourceHandler("/pages/\*\*").addResourceLocations("/pages/");
6.          registry.addResourceHandler("/css/\*\*").addResourceLocations("/css/");
7.          registry.addResourceHandler("/js/\*\*").addResourceLocations("/js/");
8.          registry.addResourceHandler("/plugins/\*\*").addResourceLocations("/plugins/");
9.      }
10. }

保证被加载

1.  @Configuration
2.  @ComponentScan({"com.itheima.controller","com.itheima.config"})
3.  @EnableWebMvc
4.  public class SpringMvcConfig {
5.  }

##### 列表页

发送异步请求

1.              methods: {
2.                  _//列表_
3.                  getAll() {
4.                      _//发送ajax请求_
5.                      axios.get("/books").then((res)=>{
6.                          this.dataList = res.data.data;
7.                      });
8.                  },
9.              }

##### 添加页

1.                  _//添加_
2.                  handleAdd () {
3.                      _//发送ajax请求_
4.                      axios.post("/books",this.formData).then((res)=>{
5.                          console.log(res.data);
6.                          _//如果操作成功，关闭弹层，显示数据_

7.                              this.dialogFormVisible = false;
8.                           this.getAll();
9.                     });
10.                 },

区分操作成功/失败的情况

1.                  _//添加_
2.                  handleAdd () {
3.                      _//发送ajax请求_
4.                      axios.post("/books",this.formData).then((res)=>{
5.                          console.log(res.data);
6.                          _//如果操作成功，关闭弹层，显示数据_
7.                          if(res.data.code == 20011){
8.                              this.dialogFormVisible = false;
9.                              this.$message.success("添加成功");
10.                         }else if(res.data.code == 20010){
11.                             this.$message.error("添加失败");
12.                         }else{
13.                             this.$message.error(res.data.msg);
14.                         }
15.                     }).finally(()=>{
16.                         this.getAll();
17.                     });
18.                 },

$message - Element UI库提供的消息提示组件

Axios补充：

axios.post() - 使用axios发送POST请求方法

这是axios库提供的用于发送POST请求的函数

"/books" - 请求的目标URL路径

这是一个相对路径，会发送到当前域名下的/books端点

对应后端的图书添加接口

this.formData - 请求体数据

this指向Vue实例

formData是Vue实例中的数据属性，包含表单输入的数据

包含图书的类别(type)、名称(name)和描述(description)

.then((res) => { - Promise回调函数

当POST请求成功完成时执行

res参数包含服务器返回的响应数据（只是一个参数变量名）

##### 弹出编辑窗口

1.                  _//弹出编辑窗口_
2.                  handleUpdate(row) {
3.                      _// console.log(row);   //row.id 查询条件_
4.                      _//查询数据，根据id查询_
5.                      axios.get("/books/"+row.id).then((res)=>{
6.                          _// console.log(res.data.data);_
7.                          if(res.data.code == 20041){
8.                              _//展示弹层，加载数据_
9.                              this.formData = res.data.data;
10.                             this.dialogFormVisible4Edit = true;
11.                         }else{
12.                             this.$message.error(res.data.msg);
13.                         }
14.                     });
15.                 },

前台中

slot-scope="scope" 是 Element UI 表格组件提供的作用域插槽

scope.row 代表当前行的数据对象

1.  <el-table-column label="操作" align="center">
2.      <template slot-scope="scope">
3.          <el-button type="primary" size="mini" @click="handleUpdate(scope.row)">编辑</el-button>
4.          <el-button type="danger" size="mini" @click="handleDelete(scope.row)">删除</el-button>
5.      </template>
6.  </el-table-column>

Row对象来自于表格的 :data="dataList" 属性

##### 编辑

1.                  _//编辑_
2.                  handleEdit() {
3.                      _//发送ajax请求_
4.                      axios.put("/books",this.formData).then((res)=>{
5.                          _//如果操作成功，关闭弹层，显示数据_
6.                          if(res.data.code == 20031){
7.                              this.dialogFormVisible4Edit = false;
8.                              this.$message.success("修改成功");
9.                          }else if(res.data.code == 20030){
10.                             this.$message.error("修改失败");
11.                         }else{
12.                             this.$message.error(res.data.msg);
13.                         }
14.                     }).finally(()=>{
15.                         this.getAll();
16.                     });
17.                 },

与添加操作几乎完全一致，除了ajax请求的类型

##### 删除

1.                  _// 删除_
2.                  handleDelete(row) {
3.                      _//1.弹出提示框_
4.                      this.$confirm("此操作永久删除当前数据，是否继续？","提示",{
5.                          type:'info'
6.                      }).then(()=>{
7.                          _//2.做删除业务_
8.                          axios.delete("/books/"+row.id).then((res)=>{
9.                              if(res.data.code == 20021){
10.                                 this.$message.success("删除成功");
11.                             }else{
12.                                 this.$message.error("删除失败");
13.                             }
14.                         }).finally(()=>{
15.                             this.getAll();
16.                         });
17.                     }).catch(()=>{
18.                         _//3.取消删除_
19.                         this.$message.info("取消删除操作");
20.                     });
21.                 }

### 拦截器

#### 拦截器概念

- 拦截器（Intercepetor）是一种动态拦截方法调用的机制，在SpringMVC中动态拦截控制器方法的执行
- 作用：
- 在指定的方法调用前后执行预先设定的代码
- 阻止原始方法的执行
- 拦截器与过滤器区别
- 归属不同：Filter属于Servlet技术，Interceptor属于SpringMVC技术
- 拦截内容不同：Filter对所有访问进行增强，Interceptor仅针对SpringMVC的访问进行增强

拦截器执行流程

—preHandle—return——controller—postHandle—afterCompletion

true

#### 入门案例

拦截器可以在方法的前/后执行

制作拦截器功能类

Controller-interceptor-ProjectInterceptor 拦截器服务于表现层

1.  @Component
2.  _//定义拦截器类，实现HandlerInterceptor接口_
3.  _//注意当前类必须受Spring容器控制_
4.  public class ProjectInterceptor implements HandlerInterceptor {
5.      @Override
6.      _//原始方法调用前执行的内容_
7.      _//返回值类型可以拦截控制的执行，true放行，false终止_
8.      public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
9.          String contentType = request.getHeader("Content-Type");
10.         HandlerMethod hm = (HandlerMethod)handler;
11.         System.out.println("preHandle..."+contentType);
12.         return true;
13.     }

14.     @Override
15.     _//原始方法调用后执行的内容_
16.     public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
17.         System.out.println("postHandle...");
18.     }

19.     @Override
20.     _//原始方法调用完成后执行的内容_
21.     public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
22.         System.out.println("afterCompletion...");
23.     }
24. }

使用false可以终止原始操作的执行

配置拦截器的执行位置

SpringMvcSupport

1.  @Configuration
2.  public class SpringMvcSupport extends WebMvcConfigurationSupport {
3.      @Autowired
4.      private ProjectInterceptor projectInterceptor;

5.      @Override
6.  _//过滤静态资源_
7.      protected void addResourceHandlers(ResourceHandlerRegistry registry) {
8.          registry.addResourceHandler("/pages/\*\*").addResourceLocations("/pages/");
9.     }

10.     @Override
11.     protected void addInterceptors(InterceptorRegistry registry) {
12.         _//配置拦截器_
13.         registry.addInterceptor(projectInterceptor).addPathPatterns("/books","/books/\*");
14.     }
15. }

该拦截器在调用books 和 /books/\* 时拦截，路径可以通过可变参数设置多个

设置扫包

1.  @Configuration
2.  @ComponentScan({"com.itheima.controller"，com.itheima.config})
3.  @EnableWebMvc
4.  _//实现WebMvcConfigurer接口可以简化开发，但具有一定的侵入性_
5.  public class SpringMvcConfig implements WebMvcConfigurer {
6.      }
7.  }

##### 简化开发（侵入性强）

1.  @Configuration
2.  @ComponentScan({"com.itheima.controller"})
3.  @EnableWebMvc
4.  _//实现WebMvcConfigurer接口可以简化开发，但具有一定的侵入性_
5.  public class SpringMvcConfig implements WebMvcConfigurer {
6.      @Autowired
7.      private ProjectInterceptor projectInterceptor;
8.      @Autowired
9.      private ProjectInterceptor2 projectInterceptor2;

10.     @Override
11.     public void addInterceptors(InterceptorRegistry registry) {
12.         _//配置多拦截器_
13.         registry.addInterceptor(projectInterceptor).addPathPatterns("/books","/books/\*");
14.     }
15. }

#### 拦截器参数

前置处理

public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {}

Request：请求对象

Response：响应对象

Handler：被调用的处理器对象，本质上是一个方法对象，对反射技术中的method对象进行了再包装

后置处理

public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {}

ModelAndView如果处理器执行完成具有返回结果，可以读取到对应数据与页面信息，并进行调整

完成后处理

public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {}

ex：如果处理器执行过程中出现异常对象，可以针对异常情况进行单独处理

但可以通过SpringMVC的异常处理机制完美替换

#### 拦截器链

当配置多个拦截器时，形成拦截器链

拦截器链的运行顺序参照拦截器添加顺序为主

PreHandle：与配置顺序相同，必定运行

PostHandle：与配置顺序相反，可能不运行

AfterCompletion：与配置顺序相反，可能不运行

## Maven Advanced

### 分模块开发

将原始模块按照功能拆分成若干个子模块，方便模块间的互相调用，接口共享

#### 创建Maven模块

#### 书写模块代码

Maven_02_ssm

1.      _<!--依赖domain运行-->_
2.      <dependency>
3.        <groupId>com.itheima</groupId>
4.        <artifactId>maven_03_pojo</artifactId>
5.        <version>1.0-SNAPSHOT</version>
6.      </dependency>

依赖domain运行

#### 通过maven指令安装模块到本地仓库（install）

使用install下载到仓库

团队内部开发需要发布模块功能到团队内部可共享的仓库中（私服）

### 依赖管理

- 依赖指当前项目运行所需的jar，一个项目可以设置多个依赖，依赖具有传递性

#### 传递依赖

- 直接依赖：在当前项目中通过依赖配置建立的依赖关系
- 间接依赖：被以来的资源如果依赖其他资源，当前项目间接依赖其他资源

#### 依赖传递冲突问题

- 路径优先：当依赖中出现相同的资源时，层级越深，优先级越低，层级越浅，优先级越高
- 声明优先：当资源在相同层级被依赖时，配置顺序靠前（配置文件的顺序）的覆盖配置顺序靠后的
- 特殊优先：当同级配置了相同资源的不同版本，后配置的覆盖先配置的

#### 可选依赖与排除依赖

可选依赖-隐藏自己的依赖 对外隐藏当前所依赖的资源——不透明

1.          <dependency>
2.              <groupId>com.itheima</groupId>
3.              <artifactId>maven_03_pojo</artifactId>
4.              <version>1.0-SNAPSHOT</version>
5.              <!--可选依赖是隐藏当前工程所依赖的资源，隐藏后对应资源将不具有依赖传递性;-->
6.              <optional>false</optional>
7.          </dependency>

- 排除依赖是隐藏当前资源对应的依赖关系-使用其他的资源时排除不用的依赖

主动断开以来的资源，被排除的资源无需指定版本——不需要

1.        <exclusions>
2.          <exclusion>
3.            <groupId>log4j</groupId>
4.            <artifactId>log4j</artifactId>
5.          </exclusion>
6.          <exclusion>
7.            <groupId>org.mybatis</groupId>
8.            <artifactId>mybatis</artifactId>
9.          </exclusion>
10.       </exclusions>
11.     </dependency>

排除依赖仅指定GA即可，无需指定V

### 聚合与继承

#### 聚合

- 聚合：将多个模块组织成一个整体，同时进行项目构建的过程称为聚合
- 聚合工程：通常是一个不具有业务功能的空工程（有且仅有一个pom文件）
- 作用：使用聚合工程可以将多个工程编组，通过对聚合工程进行构建，实现对时所包含的模块进行同步构建
- 当工程中某个模块发生更新（变更）时，必须保障工程中与已更新模块关联的模块同步更新，此时可以使用聚合工程来解决批量模块同步构建的问题

新建maven_01_parent 设置打包类型为pom

1.      <groupId>com.itheima</groupId>
2.      <artifactId>maven_01_parent</artifactId>
3.      <version>1.0-RELEASE</version>
4.      <packaging>pom</packaging>

设置当前聚合工程所包含的子模块名称

1.      _<!--设置管理的模块名称-->_
2.      <modules>
3.          <module>../maven_02_ssm</module>
4.          <module>../maven_03_pojo</module>
5.          <module>../maven_04_dao</module>
6.      </modules>

启动compile后会先构建没有依赖的，交换module的顺序对编译过程不产生影响

#### 继承

- 描述的是两个工程间的关系，与java中的继承相似，子工程可以继承父工程中的配置信息，常见于依赖关系的继承
- 作用：简化配置/减少版本冲突
- 聚合继承一般同一个文件

Maven_02_ssm 在子工程中配置当前继承的夫工程

1.    <parent>
2.      <groupId>com.itheima</groupId>
3.      <artifactId>maven_01_parent</artifactId>
4.      <version>1.0-RELEASE</version>
5.      <relativePath>../maven_01_parent/pom.xml</relativePath>
6.    </parent>

配置父工程GAV relativePath

父工程中可选依赖 配置子工程中可选的依赖关系

1.      _<!--定义依赖管理-->_
2.      <dependencyManagement>
3.          <dependencies>
4.              <dependency>
5.                  <groupId>junit</groupId>
6.                  <artifactId>junit</artifactId>
7.                  <version>4.12</version>
8.                  <scope>test</scope>
9.              </dependency>
10.         </dependencies>
11.     </dependencyManagement>

子工程中使用父工程中的可选依赖时，仅需要提供群组id和项目id，无需提供版本，版本由父工程统一提供，避免版本冲突，子工程中还可以定义父工程中没有定义的依赖关系

#### 继承与聚合的区别

- 作用：聚合用于快速构建项目，配置用于快速配置
- 相同点：
- 聚合与继承的pom.xml文件打包方式均为pom，可以将两种关系制作到同一个pom文件中
- 聚合与继承均属于设计型模块，并无实际的模块内容
- 不同点：
- 聚合是在当前模块中配置关系，聚合可以感知到参与聚合的模块有哪些
- 继承是在子模块中配置关系，父模块无法感知哪些子模块继承了自己

### 属性管理

#### 属性

1.      _<!--定义属性-->_
2.      <properties>
3.          <spring.version>5.2.10.RELEASE</spring.version>
4.          <junit.version>4.12</junit.version>
5.          <mybatis-spring.version>1.3.0</mybatis-spring.version>
6.          _<!--<jdbc.url>jdbc:mysql://127.0.0.1:3306/ssm_db</jdbc.url>-->_
7.      </properties>

8.      _<!--定义依赖管理-->_
9.     <dependencyManagement>
10.         <dependencies>
11.             <dependency>
12.                 <groupId>junit</groupId>
13.                 <artifactId>junit</artifactId>
14.                 <version>${junit.version}</version>
15.                 <scope>test</scope>
16.             </dependency>
17.         </dependencies>
18.     </dependencyManagement>

定义属性--引用属性

#### 配置文件加载属性

加载jdbc，定义属性

1.      _<!--定义属性-->_
2.      <properties>
3.          <jdbc.url>jdbc:mysql://127.0.0.1:3306/ssm_db</jdbc.url>
4.      </properties>

Jdbc.properties配置资源中引用属性

1.  jdbc.driver=com.mysql.jdbc.Driver
2.  jdbc.url=${jdbc.url}
3.  jdbc.username=root
4.  jdbc.password=root

设置资源目录

开启资源文件目录加载属性的过滤器

1.      <build>
2.          <resources>
3.              _<!--设置资源目录，并设置能够解析${}-->_
4.              <resource>
5.                  <directory>${project.basedir}/src/main/resources</directory>
6.                  <filtering>true</filtering>
7.              </resource>
8.          </resources>
9.      </build>

${project.basedir}内置属性名

配置maven打jar包，忽略web.xml检查

1.        <plugin>
2.          <groupId>org.apache.maven.plugins</groupId>
3.          <artifactId>maven-war-plugin</artifactId>
4.          <version>3.2.3</version>
5.          <configuration>
6.            <failOnMissingWebXml>false</failOnMissingWebXml>
7.          </configuration>
8.        </plugin>

#### 版本管理

- 工程版本：
- SNAPSHOT（快照版本）

项目开发过程中临时输出的版本，称为快照版本

快照版本会随着开发的进展不断更新

- RELEASE（发布版本）

项目开发到进入阶段里程碑后，向团队外部发布较为稳定的版本，这种版本所对应的构建是稳定的，即便进行功能的后续开发，也不会改变当前发布版本内容

- 发布版本
- Alpha版
- Beta版
- 纯数字版

### 多环境配置与应用

场景：生产环境需要一个数据库，开发环境需要一个数据库，测试环境需要一个数据库则需要配置多环境

#### 多环境开发

1.  _<!--配置多环境-->_
2.      <profiles>
3.          _<!--开发环境-->_
4.          <profile>
5.              <id>env_dep</id>
6.              <properties>
7.                  <jdbc.url>jdbc:mysql://127.1.1.1:3306/ssm_db</jdbc.url>
8.              </properties>
9.              _<!--设定是否为默认启动环境-->_
10.             <activation>
11.                 <activeByDefault>true</activeByDefault>
12.             </activation>
13.         </profile>
14.         _<!--生产环境-->_
15.         <profile>
16.             <id>env_pro</id>
17.             <properties>
18.                 <jdbc.url>jdbc:mysql://127.2.2.2:3306/ssm_db</jdbc.url>
19.             </properties>
20.         </profile>
21.         _<!--测试环境-->_
22.         <profile>
23.             <id>env_test</id>
24.             <properties>
25.                 <jdbc.url>jdbc:mysql://127.3.3.3:3306/ssm_db</jdbc.url>
26.             </properties>
27.         </profile>
28.     </profiles>

选中执行指令，mvn install -p env_test 相当于携带test指令

#### 跳过测试

应用场景：功能更新中并且还没有开发完毕/快速打包/...

或者指令实现

mvn package -D skipTests

弊端：全部跳过，一个测试都不执行

配置文件实现跳过指定的测试部分/细粒度管理

1.      <build>
2.          <plugins>
3.              <plugin>
4.                  <artifactId>maven-surefire-plugin</artifactId>
5.                  <version>2.12.4</version>
6.                  <configuration>
7.                      <skipTests>false</skipTests>
8.                      _<!--排除掉不参与测试的内容-->_
9.                      <excludes>
10.                         <exclude>\*\*/BookServiceTest.java</exclude>
11.                     </excludes>
12.                 </configuration>
13.             </plugin>
14.         </plugins>
15.     </build>

### 私服

#### 私服简介

- 私服是一台独立的服务器，用于解决团队内部的资源共享与资源同步问题
- Nexus

Sonatype公司的一款maven私服产品

启动服务器：nexus.exe /run nexus

访问服务器：http：//localhost：8081

#### 私服仓库分类

|     |     |     |     |
| --- | --- | --- | --- |
| 仓库分类 | 英文名称 | 功能  | 关联操作 |
| 宿主仓库 | Hosted | 保存自主研发+第三方资源 | 上传  |
| 代理仓库 | Proxy | 代理连接中央仓库 | 下载  |
| 仓库组 | Group | 为仓库编组简化下载操作 | 下载  |

#### 资源上传

上传的位置（宿主地址）

|

Idea——本地仓库——私服

|

本地仓库配置访问私服的用户名/密码

下载的地址

1.  在Nexus中配置demo-release与demo-snapshot两个仓库

2.  Settings.xml中配置访问私服的权限
3.      _<!-- 配置访问私服的权限 -->_
4.      <server>
5.        <id>demo-snapshot</id>
6.        <username>admin</username>
7.        <password>admin</password>
8.      </server>
9.      <server>
10.        <id>demo-release</id>
11.       <username>admin</username>
12.       <password>admin</password>
13.     </server>

14.  找到group中的maven仓库作为仓库组

15.  移动demo-release与demo-snapshot得到maven-public管理

16.  配置私服的访问路径
17.       <mirror>
18.       _<!-- 私服的访问路径 -->_
19.        <mirror>
20.        <id>maven-public</id>
21.        <mirrorOf>\*</mirrorOf>
22.        <url>http://localhost:8081/repository/maven-public/</url>
23.      </mirror>
24.    </mirrors>

这样本地仓库就与私服建立联系

1.  配置当前工程保存在私服中的具体位置
2.      _<!--配置当前工程保存在私服中的具体位置-->_
3.      <distributionManagement>
4.          <repository>
5.              <id>itheima-release</id>
6.              <url>http://localhost:8081/repository/itheima-release/</url>
7.          </repository>
8.          <snapshotRepository>
9.              <id>itheima-snapshot</id>
10.             <url>http://localhost:8081/repository/itheima-snapshot/</url>
11.         </snapshotRepository>
12.     </distributionManagement>

13.  发布命令

Mvn deploy

## SpringBoot

### SpringBoot简介

SpringBoot是由Pivotal团队提供的全新框架，其设计的是用来简化Spring应用的初始搭建以及开发过程

#### 入门案例

制作controller类

1.  @RestController
2.  @RequestMapping("/books")
3.  public class BookController {

4.      @GetMapping("/{id}")
5.      public String getById(@PathVariable Integer id){
6.          System.out.println("id ==> "+id);
7.          return "hello , spring boot!";
8.      }
9. }

Application类

1.  @SpringBootApplication
2.  public class Application {

3.      public static void main(String\[\] args) {
4.          SpringApplication.run(Application.class, args);
5.      }
6.  }

SpringBoot内嵌Tomcat已经能启动

#### SpringBoot与Spring对比

最简SpringBoot程序所包含的基础文件

pom.xml

Application类

Spring程序与SpringBoot程序对比

|     |     |     |
| --- | --- | --- |
| 类/配置文件 | Spring | SpringBoot |
| Pom文件中的坐标 | 手工制作 | 勾选添加 |
| Web3.0配置类 | 手工制作 | 无   |
| Spring/SpringMVC配置类 | 手工制作 | 无   |
| 控制器 | 手工制作 | 手工制作 |

但基于idea开发Spring Boot程序需要确保联网，且能加载到程序框架结构

#### SpringBoot项目快速启动

1.  先对SpringBoot项目打包（执行Maven构建指令package）

2.  找到springboot_01_quickstart-0.0.1-SNAPSHOT文件，打开对应位置
3.  使用cmd打开输入java -jar springboot_01_quickstart-0.0.1-SNAPSHOT

（jar支持命令行启动，但需要依赖maven插件支持）

1.          <plugins>
2.              <plugin>
3.                  <groupId>org.springframework.boot</groupId>
4.                  <artifactId>spring-boot-maven-plugin</artifactId>
5.              </plugin>

成功快速启动

#### SpringBoot概述

简化Spring应用的初始搭建以及开发过程，自动配置，起步依赖，辅助功能（内置服务器）

Spring程序缺点：配置繁琐，依赖设置繁琐

起步依赖-一次性地写了若干个依赖。开发web程序所需要依赖

1.          <dependency>
2.  <groupId>org.springframework.boot</groupId>
3.              <artifactId>spring-boot-starter-web</artifactId>
4.              <exclusions>
5.                  <exclusion>
6.                     <groupId>org.springframework.boot</groupId>
7.                     <artifactId>spring-boot-starter-tomcat</artifactId>
8.                  </exclusion>
9.              </exclusions>
10.         </dependency>

Parent所有SpringBoot项目要继承的项目，定义若干个坐标版本号，以达到减少依赖冲突的目的

引导类

1.  @SpringBootApplication
2.  public class Application {

3.      public static void main(String\[\] args) {
4.          SpringApplication.run(Application.class, args);
5.      }
6.  }

SpringBoot的引导类是项目的入口，运行main方法就可以启动项目

更改Tomcat服务器

1.          <dependency>
2.              <groupId>org.springframework.boot</groupId>
3.              <artifactId>spring-boot-starter-web</artifactId>
4.              <exclusions>
5.                  <exclusion>
6.                     <groupId>org.springframework.boot</groupId>
7.                     <artifactId>spring-boot-starter-tomcat</artifactId>
8.                  </exclusion>
9.              </exclusions>
10.         </dependency>

11.         <dependency>
12.             <groupId>org.springframework.boot</groupId>
13.             <artifactId>spring-boot-starter-jetty</artifactId>
14.         </dependency>

需要先排除tomcat，更换jetty服务器（更轻量级，可扩展性更强）

### 基础配置

#### 三种配置文件

application.properties #server.port=80

application.yaml/yml

1.  server:
2.    port: 82

主写yml文件

注：自动提示功能消失解决方案：

File-Project Structure-Facets-Spring-需要配的工程-追加配置文件（yaml/yml）

加载顺序：.properties > .yml > .yaml

#### Yaml

YAML 一种数据序列化格式，容易阅读，容易与脚本语言交互，以数据为核心，重数据轻格式

##### 语法规则

- 大小写敏感
- 属性层级关系使用多行描述，每行结尾使用冒号结束
- 使用缩进表示层级关系，同层级左侧对齐，只允许使用空格
- 属性值前添加空格（属性名与属性值之间使用冒号 + 空格作为风格）
- \# 表示注释
- 数组数据在数据书写的位置下方使用减号作为数据开始符号，每行书写一个数据，减号与数据间空格风格

##### Yaml数据读取方式

Application.yaml

1.  lesson: SpringBoot

2.  server:
3.    port: 80

4.  enterprise:
5.    name: itcast
6.    age: 16
7.    tel: 4006184000
8.   subject:
9.     - Java
10.     - 前端
11.     - 大数据

Controller

方式一：使用@Value读取单一属性数据

1.  @RestController
2.  @RequestMapping("/books")
3.  public class BookController {
4.      _//使用@Value读取单一属性数据_
5.      @Value("${lesson}")
6.      private String lesson;
7.      @Value("${server.port}")
8.      private Integer port;
9.      @Value("${enterprise.subject\[0\]}")
10.     private String subject_00;

11.     @GetMapping("/{id}")
12.     public String getById(@PathVariable Integer id){
13.         System.out.println(lesson);
14.         System.out.println(port);
15.         System.out.println(subject_00);
16.         return "hello , spring boot!";
17.     }

18. }

方式二：使用Environment封装全配置数据

1.      _//使用Environment封装全配置数据_
2.      @Autowired
3.      private Environment environment;

4.          System.out.println("--------------------");
5.          System.out.println(environment.getProperty("lesson"));
6.          System.out.println(environment.getProperty("server.port"));
7.          System.out.println("---------------------");

案例：使用enterprise实体封装yaml数据

1.  _//封装yaml对象格式数据必须先声明当前实体类受Spring管控_
2.  @Component
3.  _//使用@ConfigurationProperties注解定义当前实体类读取配置属性信息，通过prefix属性设置读取哪个数据_
4.  @ConfigurationProperties(prefix = "enterprise")
5.  public class Enterprise {
6.      private String name;
7.      private Integer age;
8.      private String tel;
9.      private String\[\] subject;
10.     ...
11. }

Enterprise已有bean 可以自动装配enterprise

1.      @Autowired
2.      private Enterprise enterprise;

输出

1.          System.out.println(environment.getProperty("enterprise.age"));
2.          System.out.println(environment.getProperty("enterprise.subject\[1\]"));
3.          System.out.println(enterprise);

#### 多环境启动

##### 配置

1.  在application.yaml中配置
2.  _#设置启用的环境_
3.  spring:
4.    profiles:
5.      active: dev

6.  \---
7.  _#开发_
8.  spring:
9.   config:
10.     activate:
11.       on-profile: dev
12. server:
13.   port: 80
14. \---
15. _#生产_
16. spring:
17.   profiles: pro
18. server:
19.   port: 81
20. \---
21. _#测试_
22. spring:
23.   profiles: test
24. server:
25.   port: 82
26. \---
27. 使用.properties配置

主启动配置文件application.properties

spring.profiles.active=pro

环境分类配置文件application-dev.properties

server.port=8080

环境分类配置文件application-pro.properties

server.port=8081

##### 多环境启动命令格式

先clean再package

带参数启动SpringBoot

Java -jar springboot.jar --spring.profile.active=test

##### 多环境开发兼容问题

Maven中设置多环境属性

1.  <profiles>
2.          _<!--开发环境-->_
3.          <profile>
4.              <id>dev</id>
5.              <properties>
6.                  <profile.active>dev</profile.active>
7.              </properties>
8.          </profile>
9.          _<!--生产环境-->_
10.         <profile>
11.             <id>pro</id>
12.             <properties>
13.                 <profile.active>pro</profile.active>
14.             </properties>
15.             <activation>
16.                 <activeByDefault>true</activeByDefault>
17.             </activation>
18.         </profile>
19.         _<!--测试环境-->_
20.         <profile>
21.             <id>test</id>
22.             <properties>
23.                 <profile.active>test</profile.active>
24.             </properties>
25.         </profile>
26.     </profiles>

SpringBoot中应用Maven属性

1.  _#设置启用的环境_
2.  spring:
3.    profiles:
4.      active: ${profile.active}

Maven指令执行package指令，但没有编译，生成了对应的包，其中类参与编译，但是配置文件并没有编译，而是复制到包中

解决：对于源码中非java类对的操作要求加载Maven对应的属性，解析${}占位符

需要配置maven插件，对资源文件开启对默认占位符的解析

1.  <plugin>
2.                  <groupId>org.apache.maven.plugins</groupId>
3.                  <artifactId>maven-resources-plugin</artifactId>
4.                  <version>3.2.0</version>
5.                  <configuration>
6.                      <encoding>UTF-8</encoding>
7.                      <useDefaultDelimiters>true</useDefaultDelimiters>
8.                  </configuration>
9.              </plugin>

#### 配置文件分类

SpringBoot中4级配置文件

1级：file：config/application.yml \[最高\] （在文件位置中）

2级：file：application.yml

3级：classpath：config/application.yml （在idea中）

4级：classpath：application.yml

1级与2级留做系统打包后设置通用属性

3级与4级留做系统开发阶段设置通用属性

### 整合第三方技术

#### 整合Junit

Spring整合Junit

1.  _//设置类运行器_
2.  @RunWith(SpringJUnit4ClassRunner.class)
3.  _//设置Spring环境对应的配置类_
4.  @ContextConfiguration(classes = SpringConfig.class)
5.  public class AccountServiceTest {
6.      _//支持自动装配注入bean_
7.      @Autowired
8.      private AccountService accountService;

9.     @Test
10.     public void testFindById(){
11.         System.out.println(accountService.findById(1));
12.     }

13.     @Test
14.     public void testFindAll(){
15.         System.out.println(accountService.findAll());
16.     }
17. }

SpringBootTest整合

如果测试类在SpringBoot启动类的包或子包中，可以省略启动类的设置，也就是省略classes设定

1.  @SpringBootTest
2.  class Springboot07TestApplicationTests {

3.      @Autowired
4.      private BookService bookService;

5.      @Test
6.      public void save() {
7.          bookService.save();
8.     }

9. }

如果不放在同一包下，指定地址

1.  @SpringBootTest(classes = Springboot07TestApplication.class)

#### 整合mybatis

基于SpringBoot实现SSM整合

[Spring整合MyBatis](#_Spring整合MyBatis)

- SpringConfig
- 导入JdbcConfig
- 导入MyBatisConfig
- JdbcConfig
- 定义数据源（加载properties配置项：driver，url，username，password）
- MyBatisConfig
- 定义SqlsessionFactoryBean
- 定义映射配置

SpringBoot整合myBatis

BookDao

1.  @Mapper
2.  public interface BookDao {
3.      @Select("select \* from tbl_book where id = #{id}")
4.      public Book getById(Integer id);
5.  }

Application.yml

1.  spring:
2.    datasource:
3.      driver-class-name: com.mysql.cj.jdbc.Driver
4.      url: jdbc:mysql://localhost:3306/ssm_db?serverTimezone=UTC
5.      username: root
6.      password: root
7.      type: com.alibaba.druid.pool.DruidDataSource

type属性配置数据源 SpringBoot版本2.4.3（不含）之前需要配置timezone

### 案例：基于SpringBoot的SSM整合案例

pom.xml

配置起步依赖，必要的资源坐标

Application.yml

设置数据源，接口等

配置类

全部删除

Dao

设置@Mapper

测试类

自动生成

git sparse-checkout init --cone

git sparse-checkout set 04-springboot/code/springboot

git clone --filterblob:none https://github.com/CrRdz/Learning_SSM.git

## MyBatisPlus

### MyBatisPlus简介

- MyBatisPlus（MP）是基于MyBatis框架基础上开发的增强型工具，旨在简化开发，提高效率
- 开发方式：

基于MyBatis使用MyBatisPlus/基于Spring使用MyBatisPlus/基于SpringBoot使用MyBatisPlus

- SpringBoot整合MyBatis开发过程
- 创建SpringBoot工程
- 勾选配置使用的技术
- 设置dataSource相关属性（JDBC参数）
- 定义数据层接口映射配置

- MyBatisPlus快速入门

手动添加mp起步依赖

1.          <dependency>
2.              <groupId>com.baomidou</groupId>
3.              <artifactId>mybatis-plus-boot-starter</artifactId>
4.              <version>3.4.1</version>
5.          </dependency>

由于mp并未被收录到idea的系统内置配置，无法直接选择加入

设置jdbc参数（application.yml）

1.  spring:
2.    datasource:
3.      type: com.alibaba.druid.pool.DruidDataSource
4.      driver-class-name: com.mysql.cj.jdbc.Driver
5.      url: jdbc:mysql://localhost:3306/mybatisplus_db?serverTimezone=UTC
6.      username: root
7.      password: root

制作实体类

定义数据接口，继承BaseMapper<User>

1.  @Mapper
2.  public interface UserDao extends BaseMapper<User> {
3.  }

- MyBatisPlus特性
- 无侵入：只做增强不做改变，不会对现有工程产生影响
- 强大的CRUD操作，内置通用Mapper，少量配置即可实现单表CRUD操作
- 支持Lambda：编写查询条件无需担心字段写错
- 支持主键自动生成
- 内置分页插件

### 标准数据层开发

#### 标准数据层CRUD功能

|     |     |     |
| --- | --- | --- |
| 功能  | 自定义接口 | MP接口 |
| 新增  | boolean save（T t） | Int insert（T t） |
| 删除  | boolean delete（int id） | Int deleteById（Serializable id） |
| 修改  | boolean update（T t） | Int updateById（T t） |
| 根据id查询 | T getById（int id） | T selectById（Serializable id） |
| 查询全部 | List<T> getAll（） | List<T> selectList（） |
| 分页查询 | PageInfo<T> getAll（int page,int size） | IPage<T> selectPage（Ipage<T> page） |
| 按条件查询 | List<T> getAll（Condition condition） | IPage<T> selectPage（Wrapper<T> queryWrapper） |

#### 快速开发实体类

导入坐标

1.          <dependency>
2.              <groupId>org.projectlombok</groupId>
3.              <artifactId>lombok</artifactId>
4.              <version>1.18.12</version>
5.          </dependency>

6.  @Data
7.  @NoArgsConstructor
8.  @AllArgsConstructor
9.  public class User {
10.      private Long id;
11.      private String name;
12.      private String password;
13.      private Integer age;
14.      private String tel;
15. }

16.  @Setter
17.  @Getter
18.  @ToString

等同@Data

#### 分页查询

配置分页拦截器作为Spring管理的bean

1.  @Configuration
2.  public class MpConfig {
3.      @Bean
4.      public MybatisPlusInterceptor mpInterceptor(){
5.          _//1.定义Mp拦截器_
6.          MybatisPlusInterceptor mpInterceptor = new MybatisPlusInterceptor();
7.          _//2.添加具体的拦截器_
8.          mpInterceptor.addInnerInterceptor(new PaginationInnerInterceptor());
9.          return mpInterceptor;
10.     }
11. }

测试类中执行分页查询

1.      @Test
2.      void testGetByPage(){
3.          _//IPage对象封装了分页操作相关的数据_
4.          IPage page  = new Page(2,3);
5.          userDao.selectPage(page,null);
6.          System.out.println("当前页码值："+page.getCurrent());
7.          System.out.println("每页显示数："+page.getSize());
8.          System.out.println("一共多少页："+page.getPages());
9.          System.out.println("一共多少条数据："+page.getTotal());
10.         System.out.println("数据："+page.getRecords());
11.     }

12.  _# 开启mp的日志（输出到控制台）_
13.  mybatis-plus:
14.    configuration:
15.      log-impl: org.apache.ibatis.logging.stdout.StdOutImpl

### DQL控制

#### 条件查询方式

MyBatisPlus将书写复杂的SQL查询条件进行了封装，使用编程的形式完成查询条件的组合

1.          _//方式一：按条件查询_
2.          QueryWrapper qw = new QueryWrapper();
3.          qw.lt("age",18);
4.          List<User> userList = userDao.selectList(qw);
5.          System.out.println(userList);

6.           _//方式二：lambda格式按条件查询_
7.          QueryWrapper<User> qw = new QueryWrapper<User>();
8.          qw.lambda().lt(User::getAge, 10);
9.         List<User> userList = userDao.selectList(qw);
10.         System.out.println(userList);

11.         _//方式三：lambda格式按条件查询_
12.         LambdaQueryWrapper<User> lqw = new LambdaQueryWrapper<User>();
13.         lqw.lt(User::getAge, 10);
14.         List<User> userList = userDao.selectList(lqw);
15.         System.out.println(userList);

链式编程

1.         LambdaQueryWrapper<User> lqw = new LambdaQueryWrapper<User>();
2.          _//并且关系：10到30岁之间_
3.          _//lqw.lt(User::getAge, 30).gt(User::getAge, 10);_
4.          _//或者关系：小于10岁或者大于30岁_
5.          lqw.lt(User::getAge, 10).or().gt(User::getAge, 30);
6.          List<User> userList = userDao.selectList(lqw);
7.          System.out.println(userList);

Null值处理

1.          LambdaQueryWrapper<User> lqw = new LambdaQueryWrapper<User>();
2.          _//先判定第一个参数是否为true，如果为true连接当前条件_
3.          lqw.lt(null != uq.getAge2(),User::getAge, uq.getAge2());
4.          lqw.gt(null != uq.getAge(),User::getAge, uq.getAge());

5.          List<User> userList = userDao.selectList(lqw);
6.          System.out.println(userList);

#### 查询投影

查询结果包含属性类中部分模型

1.          _//查询投影_
2.          LambdaQueryWrapper<User> lqw = new LambdaQueryWrapper<User>();
3.          lqw.select(User::getId,User::getName,User::getAge);
4.          List<User> userList = userDao.selectList(lqw);
5.          System.out.println(userList);

使用QueryWrapper

1.          QueryWrapper<User> lqw = new QueryWrapper<User>();
2.          lqw.select("id","name","age","tel");

查询结果包含模型类中未定义的属性

1.          QueryWrapper<User> lqw = new QueryWrapper<User>();
2.          lqw.select("count(\*) as count, tel");
3.          lqw.groupBy("tel");
4.          List<Map<String, Object>> userList = userDao.selectMaps(lqw);
5.          System.out.println(userList);

如果有不支持的，去UserDao中使用原生MyBatis

#### 查询条件设定

查询条件

精确查询，查询单个

1.          LambdaQueryWrapper<User> lqw = new LambdaQueryWrapper<User>();
2.          _//等同于=_
3.          lqw.eq(User::getName,"Jerry").eq(User::getPassword,"jerry");
4.          User loginUser = userDao.selectOne(lqw);
5.          System.out.println(loginUser);

范围查询

1.          LambdaQueryWrapper<User> lqw = new LambdaQueryWrapper<User>();
2.          _//范围查询 lt le gt ge eq between_
3.          lqw.between(User::getAge,10,30);
4.          List<User> userList = userDao.selectList(lqw);
5.          System.out.println(userList);

前面小值后面大值

模糊匹配

1.          LambdaQueryWrapper<User> lqw = new LambdaQueryWrapper<User>();
2.          _//模糊匹配 like_
3.          lqw.likeLeft(User::getName,"J");
4.          List<User> userList = userDao.selectList(lqw);
5.          System.out.println(userList);

#### 字段映射与表名映射

##### 问题一：表字段与编码属性设计不同步

@TableFiled 属性注解 模型类属性定义上方

设置当前属性对应的数据表中的字段关系

@TableField（value= “pwd”）

##### 问题二：编码中添加了数据库中未定义的属性

@TableFiled（exist = false）设置属性在数据库字段中是否存在，默认为true，此属性无法与value合并使用

##### 问题三：采用默认查询开放了更多的字段查看权限

@TableFiled（select = false）设置属性是否参与查询，与select（）映射配置不冲突

问题四：表名与编码开发设计不同步

@TableName（“”）设置当前类与表格的关系

### DML控制

#### id生成策略控制

不同的表应用不同的id生成策略

- 日志：自增（1，2，3，4，...）
- 购物订单：特殊规则（FQ23948AK3843）
- 外卖单：关联地区日期等信息（10 04 20200314 34 91）
- 关联表：可省略id

...

@TableId

位置：模型类中用于表示主键的属性定义上方

作用：设置当前类中主键属性的生成策略

@TableId(type = IdType.XXXXX)

属性值选择：

AUTO（0）：使用数据库id自增策略控制id生成

NONE（1）：不设置id生成策略

INPUT（2）：用户手工输入id

ASSIGN_ID（3）：雪花算法生成id（可兼容数值型与字符串型）

ASSIGN_UUID（4）：以UUID生成算法作为id生成策略

1.  mybatis-plus:
2.    configuration:
3.      log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
4.    global-config:
5.      banner: false
6.      db-config:
7.        id-type: assign_id
8.         table-prefix: tbl_

yml设定全局设定，让每一个实体类都使用相同的策略

使用prefix全局设定表名前缀

#### 多记录操作

##### 根据主键删除多条记录/根据主键查询多条记录

1.          _//删除指定多条数据_
2.          List<Long> list = new ArrayList<>();
3.          list.add(1402551342481838081L);
4.          list.add(1402553134049501186L);
5.          list.add(1402553619611430913L);
6.          userDao.deleteBatchIds(list);
7.          _//查询指定多条数据_
8.          List<Long> list = new ArrayList<>();
9.          list.add(1L);
10.         list.add(3L);
11.         list.add(4L);
12.         userDao.selectBatchIds(list);

##### 逻辑删除

例如员工离职，但是不能删除对应员工业绩

删除操作业务问题：业务数据从数据库中丢弃

逻辑删除：为数据设置是否可用状态字段，删除时设置状态字段为不可用状态，数据保留在数据库中

1.      _//逻辑删除字段，标记当前记录是否被删除_
2.      @TableLogic(value = "0" ,delval = "1")
3.      private Integer deleted;

但进行查询操作时，会默认查询没有被逻辑删除的部分

对于Line2的优化：

1.        _# 逻辑删除字段名_
2.        logic-delete-field: deleted
3.        _# 逻辑删除字面值：未删除为0_
4.        logic-not-delete-value: 0
5.        _# 逻辑删除字面值：删除为1_
6.        logic-delete-value: 1

在yaml中配置逻辑删除字段名与删除字面值

##### 乐观锁

业务并发现象带来的问题：秒杀

1.      @Version
2.      private Integer version;

实现乐观锁

1.  @Configuration
2.  public class MpConfig {
3.      @Bean
4.      public MybatisPlusInterceptor mpInterceptor() {
5.          _//1.定义Mp拦截器_
6.          MybatisPlusInterceptor mpInterceptor = new MybatisPlusInterceptor();
7.          _//2.添加具体的拦截器_
8.          mpInterceptor.addInnerInterceptor(new PaginationInnerInterceptor());
9.          _//3.添加乐观锁拦截器_
10.         mpInterceptor.addInnerInterceptor(new OptimisticLockerInnerInterceptor());
11.         return mpInterceptor;
12.     }
13. }

添加乐观锁

1.      @Test
2.      void testUpdate(){

3.          _//1.先通过要修改的数据id将当前数据查询出来_
4.          User user = userDao.selectById(3L);     _//version=3_
5.          User user2 = userDao.selectById(3L);    _//version=3_

6.          user2.setName("Jock aaa");
7.          userDao.updateById(user2);              _//version=>4_

8.          user.setName("Jock bbb");
9.          userDao.updateById(user);               _//verion=3?条件不成立_
10.      }

使用乐观锁机制再修改前必须先获取到对应数据的version方可正常进行

### 快速开发

代码生成器

模板：由MyBatisPlus提供

数据库相关配置：读取数据库获取信息

开发者自定义配置：手工配置

1.          _<!--代码生成器-->_
2.          <dependency>
3.              <groupId>com.baomidou</groupId>
4.              <artifactId>mybatis-plus-generator</artifactId>
5.              <version>3.4.1</version>
6.          </dependency>

7.          _<!--velocity模板引擎-->_
8.          <dependency>
9.             <groupId>org.apache.velocity</groupId>
10.             <artifactId>velocity-engine-core</artifactId>
11.             <version>2.3</version>
12.         </dependency>

Generator

1.  public class CodeGenerator {
2.      public static void main(String\[\] args) {
3.          _//1.获取代码生成器的对象_
4.          AutoGenerator autoGenerator = new AutoGenerator();

5.          _//设置数据库相关配置_
6.          DataSourceConfig dataSource = new DataSourceConfig();
7.          dataSource.setDriverName("com.mysql.cj.jdbc.Driver");
8.          dataSource.setUrl("jdbc:mysql://localhost:3306/mybatisplus_db?serverTimezone=UTC");
9.         dataSource.setUsername("root");
10.         dataSource.setPassword("root");
11.         autoGenerator.setDataSource(dataSource);

12.         _//设置全局配置_
13.         GlobalConfig globalConfig = new GlobalConfig();
14.         globalConfig.setOutputDir(System.getProperty("user.dir")+"/mybatisplus_04_generator/src/main/java");    _//设置代码生成位置_
15.         globalConfig.setOpen(false);    _//设置生成完毕后是否打开生成代码所在的目录_
16.         globalConfig.setAuthor("黑马程序员");    _//设置作者_
17.         globalConfig.setFileOverride(true);     _//设置是否覆盖原始生成的文件_
18.         globalConfig.setMapperName("%sDao");    _//设置数据层接口名，%s为占位符，指代模块名称_
19.         globalConfig.setIdType(IdType.ASSIGN_ID);   _//设置Id生成策略_
20.         autoGenerator.setGlobalConfig(globalConfig);

21.         _//设置包名相关配置_
22.         PackageConfig packageInfo = new PackageConfig();
23.         packageInfo.setParent("com.aaa");   _//设置生成的包名，与代码所在位置不冲突，二者叠加组成完整路径_
24.         packageInfo.setEntity("domain");    _//设置实体类包名_
25.         packageInfo.setMapper("dao");   _//设置数据层包名_
26.         autoGenerator.setPackageInfo(packageInfo);

27.         _//策略设置_
28.         StrategyConfig strategyConfig = new StrategyConfig();
29.         strategyConfig.setInclude("tbl_user");  _//设置当前参与生成的表名，参数为可变参数_
30.         strategyConfig.setTablePrefix("tbl_");  _//设置数据库表的前缀名称，模块名 = 数据库表名 - 前缀名  例如： User = tbl_user - tbl__
31.         strategyConfig.setRestControllerStyle(true);    _//设置是否启用Rest风格_
32.         strategyConfig.setVersionFieldName("version");  _//设置乐观锁字段名_
33.         strategyConfig.setLogicDeleteFieldName("deleted");  _//设置逻辑删除字段名_
34.         strategyConfig.setEntityLombokModel(true);  _//设置是否启用lombok_
35.         autoGenerator.setStrategy(strategyConfig);
36.         _//2.执行生成操作_
37.         autoGenerator.execute();
38.     }
39. }

