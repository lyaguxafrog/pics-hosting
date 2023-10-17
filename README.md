# pics-hosting

## Установка

1. Склонируйте репозиторий 
```
gh repo clone lyaguxafrog/pics-hosting && cd pics-hosting
```

2. Установите [Docker](https://docs.docker.com/desktop/?_gl=1*1dvsgbs*_ga*MzMwMzI5NDM0LjE2OTQwOTgyMjE.*_ga_XJWPQMJYHQ*MTY5NzUyNjAwMy44LjEuMTY5NzUyNjAyMC40My4wLjA.) и [Docker-compose](https://docs.docker.com/compose/)


3. Настройте конфиг:
```bash
./helper.sh config
```

**Не забудьте сменить SECRET_KEY в `kernel/.env`!**


## Деплой

Для запуска приложения используйте команду:

```bash
./deploy.sh
```
По умолчанию логин и пароль в админ-панель `admin`:`admin`. **Обязательно смените его!**
