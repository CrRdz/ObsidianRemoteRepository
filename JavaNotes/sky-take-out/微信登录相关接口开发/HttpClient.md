HttpClient是Apahe Jakarta Common下的子项目 可以用来提供高效的最新的 功能丰富的支持HTTP协议的客户端编程工具包 并且它支持HTTP协议最新的版本和建议
核心API：
- HttpClient
- HttpClients
- CloseableHttpClient
- HttpGet
- HttpPost
发送请求步骤
- 创建HttpClient对象
- 创建Http请求对象
- 调用HttpClient的execute方法发送请求
# 入门案例
```java
@SpringBootTest
public class HttpClientTest{
	/**
	* 测试通过httpclient发送get方式的请求
	*/
	@Test
	public void testGet() throws Exception{
	// 创建httpclient对象
	CloseableHttpClient httpclient = HttpClients.createDefault();
	
	// 发送请求 接受响应结果
	CloseableHttpResponse response = httpClient.exexute(httpGET);
	
	// 获取服务端返回的状态码
	int statusCode = response.getStatusLine().getStatusCode();
	System.out.println("服务端返回的状态码为：" + statusCode);
	
	HttpEntity entity = response.getEntity();
	String body = EntityUtils.toString(entity);
	System.out.println("服务端返回的数据为" + body);
	
	// 关闭资源
	response.close();
	httpClient.close();
	}

}
```