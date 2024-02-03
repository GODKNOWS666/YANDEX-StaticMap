from api_func import show_image, get_map_image_by_geocode, get_map_image_by_ll_z

image = get_map_image_by_ll_z(input(), int(input()))
show_image(image)
print(1)