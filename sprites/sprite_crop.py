from PIL import Image

def del_border(path, type_save="save", new_name=""):
    if "." not in new_name: new_name = new_name + ".png"
    sheet = Image.open(path)

    data = sheet.load()
    crop_coords = []
    for y1 in range(sheet.size[1]):
        if list(filter(lambda x: x != 0, map(lambda x: data[x, y1][3], range(sheet.size[0])))) != []:
            crop_coords.append(y1)
            break
    for x1 in range(sheet.size[0]):
        if list(filter(lambda y: y != 0, map(lambda y: data[x1, y][3], range(sheet.size[1])))) != []:
            crop_coords.append(x1)
            break
    for x2 in range(sheet.size[0]-1, 0, -1):
        if list(filter(lambda y: y != 0, map(lambda y: data[x2, y][3], range(sheet.size[1]-1, -1, -1)))) != []:
            crop_coords.append(x2)
            break
    for y2 in range(sheet.size[1]-1, 0, -1):
        # print(list(filter(lambda x: x != 0, map(lambda x: data[x, y2][3], range(sheet.size[0]-1, -1, -1)))))
        if list(filter(lambda x: x != 0, map(lambda x: data[x, y2][3], range(sheet.size[0]-1, -1, -1)))) != []:
            crop_coords.append(y2)
            break
    print("coords to crop:", *crop_coords)
    sheet = sheet.crop(crop_coords)

    print("/".join(path.split("/")[:-1]))
    if type_save == "save":
        sheet.save("/".join(path.split("/")[:-1]+[new_name]))
    elif type_save == "replace":
        sheet.save(path)


def sprite_crop(path, type_sprites, sprite, grid, inacurr=[0, 0, 0, 0], sep=(), single_inacurr={}, name=""):
    path = path.replace("\\", "/")
    sheet = Image.open(path)
    if name == "":
        name = path.split("/")[-1].split(".")[0]
        if name[0] == "_": name = name[1:]
    print(path)
    print(name)

    if len(inacurr) == 0: inacurr = [0, 0, 0, 0]
    elif len(inacurr) == 1: inacurr += [0, inacurr[0], 0]
    elif len(inacurr) == 2: inacurr += [inacurr[0], inacurr[1]]
    elif len(inacurr) == 3:  inacurr += [inacurr[1]]
    for k, v in single_inacurr.items():
        if len(v) == 0: single_inacurr[k] = [0, 0, 0, 0]
        elif len(v) == 1: single_inacurr[k] += [0, v[0], 0]
        elif len(v) == 2: single_inacurr[k] += [v[0], v[1]]
        elif len(v) == 3: single_inacurr[k] += [v[1]]

    if sep == None or sep == (): sep = (sheet.size[0]//grid[1], sheet.size[1]//grid[0])
    print("sep:", sep)
    count = 0
    for y in range(1, grid[0] + 1):
        for x in range(1, grid[1] + 1):
            res_x = x * sep[0]
            res_y = y * sep[1]
            res_x1 = res_x-sep[0]+(sep[0]-sprite[0])/2 + inacurr[0]
            res_y1 = res_y-sep[1]+(sep[1]-sprite[1])/2 + inacurr[1]
            res_x2 = res_x-(sep[0]-sprite[0])/2 + inacurr[2]
            res_y2 = res_y-(sep[1]-sprite[1])/2 + inacurr[3]
            for k, v in single_inacurr.items():
                if k[1]+1 == x and k[0]+1 == y:
                    res_x1 += v[0]
                    res_y1 += v[1]
                    res_x2 += v[2]
                    res_y2 += v[3]
            icon = sheet.crop((res_x1, res_y1, res_x2, res_y2))
            print("/".join(path.split("/")[:-1] + [name + f"_{type_sprites[y - 1]}_{count}.png"]))
            icon.save("/".join(path.split("/")[:-1]+[name+f"_{type_sprites[y-1]}_{count}.png"]))
            count += 1
        count = 0

sprite_crop(r"C:\Users\maxim\Desktop\SASHA\PROJECTS\Office_Nightmare_versions\PyGame\sprites\character\base_choice\walk\_down_walk.png",
            type_sprites=["", "1"], name="walk",
            sprite=(20, 35), grid=(2, 4),
            inacurr=[0], sep=())
# del_border("character/choice1/death/death.png", type_save="save", new_name="crop_death.png")