
import os

def save_image(user_id, image_name, file_path, image_password):
    # Создаем папку imgs/ для хранения изображений, если она не существует
    if not os.path.exists("imgs"):
        os.makedirs("imgs")

    # Генерируем уникальное имя файла, основанное на идентификаторе пользователя и имени изображения
    unique_filename = f"{user_id}_{image_name}.jpg"

    # Сохраняем изображение в папку imgs/ с уникальным именем
    with open(os.path.join("imgs", unique_filename), "wb") as img_file:
        with open(file_path, "rb") as original_file:
            img_file.write(original_file.read())

    if image_password:
        # Если у изображения есть пароль, сохраняем его в отдельный файл
        with open(os.path.join("imgs", f"{unique_filename}.password"), "w") as password_file:
            password_file.write(image_password)
