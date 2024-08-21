# stalcraft.net-checker-log-pass
stalcraft.net checker log:pass REQUESTS 

ЧЕКЕР РАБОТАЕТ НА РЕШЕНИЕ КАПЧИ - https://anti-captcha.com/  
Инструкция по запуску:  
1. Кидаем все файлы с этого репозитория в любую папку
2. Вводим апи ключ anti-captcha и количество потоков   
![image](https://github.com/user-attachments/assets/c2de704f-89e1-4a71-8d0b-a18083b05746)
3. Заполняем аккаунтами наш файл accounts.txt и кидаем прокси в файл proxies.txt (формат ip:port:login:password)
4. Пишем cmd в папке  
  ![image](https://github.com/user-attachments/assets/26d501ae-712a-4edc-bbbb-c828ee3f5924)  
5. Открывается консоль и мы туда пишем pip install -r requirements.txt  
6. Пишем python main.py  

Функционал:  
Решение капчи через anti-captcha
Поддержка socks5/http прокси ip:port:log:password / ip:port
Многопоточность      
Парс на платную подписку в аккаунте    

![image](https://github.com/user-attachments/assets/12326789-b294-4db6-a6af-5b0862b0096d)

