# rest_framework_tutorial
superuser:  
 administrator  
 12345678  

由于还没有设置任何身份验证类，所以应用默认的`SessionAuthentication`和`BasicAuthentication`  
因此，如果通过代码与API交互，我们需要在每次请求上显示提供身份验证凭据  
`http -a administrator:12345678 POST http://127.0.0.1:8000/snippets/ code="print(123)"`  
