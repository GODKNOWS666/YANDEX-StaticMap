import requests
from io import BytesIO
import pygame

STATIC_API_URL = "http://static-maps.yandex.ru/1.x/"
GEOCODER_API_URL = "http://geocode-maps.yandex.ru/1.x/"
GEOCODER_API_KEY = "40d1649f-0493-4b70-98ba-98533de7710b"


def get_map_image_by_geocode(geocode: str, index=0, add_point=False, autoscale=False):
    geocoder_params = {
        "apikey": GEOCODER_API_KEY,
        "geocode": geocode,
        "format": "json"
    }

    response = requests.get(GEOCODER_API_URL, geocoder_params).json()
    members = response["response"]["GeoObjectCollection"]["featureMember"]

    # Рамка вокруг объекта:
    envelope = members[index]["GeoObject"]["boundedBy"]["Envelope"]

    # левая, нижняя, правая и верхняя границы из координат углов:
    top_left = envelope["upperCorner"].split(" ")
    bottom_right = envelope["lowerCorner"].split(" ")

    static_api_params = {
        "l": "map",
        "ll": ",".join(top_left),
        "bbox": ",".join(top_left) + '~' + ",".join(bottom_right)
    }

    if add_point:
        point = [float(val) for val in members[index]
        ["GeoObject"]["Point"]["pos"].split(" ")]
        static_api_params["pt"] = f"{point[0]},{point[1]},pm2rdm"

    if autoscale:
        static_api_params["spn"] = calculate_scale(top_left, bottom_right)

    response = requests.get(STATIC_API_URL, static_api_params)
    return response.content


def get_map_image_by_ll_z(lll, zz):
    geocoder_params = {
        "l": 'map',
        "ll": lll,
        "z": str(zz),
    }

    response = requests.get(STATIC_API_URL, geocoder_params)
    return response.content


def calculate_scale(top_left: tuple, bottom_right: str):
    # Вычисляем полуразмеры по вертикали и горизонтали
    dx = round(abs(float(top_left[1]) - float(bottom_right[1])) / 2.0, 5)
    dy = round(abs(float(top_left[0]) - float(bottom_right[0])) / 2.0, 5)

    span = f"{dx},{dy}"
    return span


# def show_image(image_data):
#    pygame.init()
#    image = pygame.image.load(BytesIO(image_data))
#    image_rect = image.get_rect()
#    width, height = image_rect[2], image_rect[3]
#    screen = pygame.display.set_mode((width, height))
#    screen.blit(image, (0, 0))
#    running = True
#    while running:
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                return
#        pygame.display.flip()


def show_image(image_data, ll, z):
    z = int(z)
    ll1, ll2 = tuple(map(float, ll.split(',')))
    pygame.init()
    image = pygame.image.load(BytesIO(image_data))
    image_rect = image.get_rect()
    width, height = image_rect[2], image_rect[3]
    screen = pygame.display.set_mode((width, height))
    screen.blit(image, (0, 0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    if z < 21:
                        z += 1
                        image = pygame.image.load(BytesIO(get_map_image_by_ll_z(ll, z)))
                        screen.blit(image, (0, 0))
                elif event.key == pygame.K_PAGEDOWN:
                    if z > 0:
                        z -= 1
                        image = pygame.image.load(BytesIO(get_map_image_by_ll_z(ll, z)))
                        screen.blit(image, (0, 0))
                elif event.key == pygame.K_UP:
                    ll1 += 5
                    print(ll1)
                    image = pygame.image.load(BytesIO(get_map_image_by_ll_z(f'{ll1},{ll2}', z)))
                    screen.blit(image, (0, 0))
                elif event.key == pygame.K_DOWN:
                    ll1 -= 5
                    print(ll1)
                    image = pygame.image.load(BytesIO(get_map_image_by_ll_z(f'{ll1},{ll2}', z)))
                    screen.blit(image, (0, 0))
                elif event.key == pygame.K_RIGHT:
                    ll2 += 5
                    print(ll2)
                    image = pygame.image.load(BytesIO(get_map_image_by_ll_z(f'{ll1},{ll2}', z)))
                    screen.blit(image, (0, 0))
                elif event.key == pygame.K_LEFT:
                    ll2 -= 5
                    print(ll2)

                    image = pygame.image.load(BytesIO(get_map_image_by_ll_z(f'{ll1},{ll2}', z)))
                    screen.blit(image, (0, 0))
        pygame.display.flip()


ll, z = input(), int(input())
image = get_map_image_by_ll_z(ll, z)
show_image(image, ll, z)
