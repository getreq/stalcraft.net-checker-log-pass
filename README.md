# stalcraft.net-checker-log-pass
stalcraft.net checker log:pass REQUESTS 

ЧЕКЕР РАБОТАЕТ НА РЕШЕНИЕ КАПЧИ - https://anti-captcha.com/  
Инструкция по запуску:  
1. Кидаем все файлы с этого репозитория в любую папку
2. Вводим апи ключ anti-captcha и количество потоков   
 ![image](https://github.com/user-attachments/assets/ef3767a8-7eb1-40d4-9298-d453588ed6bb)  
3. Заполняем аккаунтами наш файл accounts.txt и кидаем прокси в файл proxies.txt (формат ip:port:login:password)
4. Пишем cmd в папке  
  ![image](https://github.com/user-attachments/assets/26d501ae-712a-4edc-bbbb-c828ee3f5924)  
5. Открывается консоль и мы туда пишем pip install -r requirements.txt  
6. Пишем python main.py  

Функционал:  
Решение капчи через anti-captcha
Поддержка socks5 прокси ip:port:log:password    
Многопоточность      
Парс на платную подписку в аккаунте    

![image](https://github.com/user-attachments/assets/eabff694-f243-41e8-9731-94bfa900f110)

