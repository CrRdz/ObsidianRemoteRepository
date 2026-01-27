前后端分离开发流程： 定制接口 - 前端开发/后端开发 - 联调（校验格式） - 提测（提测）

---

- 使用Swagger你只需要按照它的规范去定义接口以及接口相关的信息 就可以做到生成接口文档 以及在线接口调试页面 (https://swagger.io)
- Knife4j 是为Java MVC框架集成Swagger生成API文档的增强解决方案
- 导入Maven坐标
	```xml
	<dependency>  
	    <groupId>com.github.xiaoymin</groupId>  
	    <artifactId>knife4j-spring-boot-starter</artifactId>  
	    <version>${knife4j}</version>  
	</dependency>
	```
- 在配置类`WebMvcConfiguration`中加入knife4j相关配置
```java
/**  
 * 设置静态资源映射  
 * @param registry  
 */  
	protected void addResourceHandlers(ResourceHandlerRegistry registry) {  
	    registry.addResourceHandler("/doc.html").addResourceLocations("classpath:/META-INF/resources/");  
	registry.addResourceHandler("/webjars/**").addResourceLocations("classpath:/META-INF/resources/webjars/");  
}
```
- 设置静态资源映射 否则接口文档页面无法访问
```java
	/**  
	 * 通过knife4j生成接口文档  
	 * @return  
	 */  
	@Bean  
	public Docket docket() {  
	    ApiInfo apiInfo = new ApiInfoBuilder()  
            .title("苍穹外卖项目接口文档")  
            .version("2.0")  
            .description("苍穹外卖项目接口文档")  
            .build();  
    Docket docket = new Docket(DocumentationType.SWAGGER_2)  
            .apiInfo(apiInfo)  
            .select()  
            .apis(RequestHandlerSelectors.basePackage("com.sky.controller"))  
            .paths(PathSelectors.any())  
            .build();  
    return docket;  
	}
```
Postman / YAPI ...是设计阶段使用的工具 管理和维护接口
Swagger在开发阶段使用的框架 帮助后端开发人员做后端的接口测试
# 常用注解
通过注解可以控制生成的接口文档 使接口文档有更好的可读性 常用注解如下
`@API` 用在类上 例如Controller 表示对类的说明
`@ApiModel` 用在类上 例如entity DTO VO
`@ApiModelProperty` 用在属性上 描述属性信息
`ApiOperation` 用在方法上 例如Controller 方法 说明 方法的用途和作用