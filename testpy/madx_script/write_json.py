import json

bapp = ["id1273162445","id1354796403","id1413608864","id1435277159","id1437231299","id1446728841","id1453795744","id1459499304","id1461463973","id1461700291","id1466213245","id1466588301","id1473573813","id1478589337","id1480361496","id1481316255","id1488072475","id1492964317","id1519397914","id1519746792","id1531670603","id1533641021","id1544699237","id1560608260","id1563159261","id1565310917","id1092689152","com.beitakeji.zhipai","com.bettagames.wordbuddies","com.chaos.mergera","com.dragonmonster.idlefarmadventure.free","com.fillword.cross.wordmind.en","com.fotoable.mergetown","com.fotoable.MergicalHome","com.fotoable.NutsPoker","com.fotoable.palette","com.fotoable.townest","com.fotoable.villascrusher","com.fotoable.wordvilla.de","com.fotoable.WordVillas","com.island.card","com.jigsaw.wordplus","com.restaurant.rush.cookinggame.fever.frenzy","com.slots.free.vegas.casino.jackpotland","com.sports.real.disc.golf.online","com.sports.real.golf.rival.online","com.starfish.wordfrench.an","com.starfish.wordjp.an","com.tangramgames.gourddoll.wordcrush","com.tankgame.tankhero.en","com.wordfind.wortschau.de","com.wordgame.cross.android.en","com.wordgame.newcross.android.en","com.wordhome.newcross.android.en","com.fanatee.cody","id1273162445","id1354796403","id1413608864","id1435277159","id1437231299","id1446728841","id1453795744","id1459499304","id1461463973","id1461700291","id1466213245","id1466588301","id1473573813","id1478589337","id1480361496","id1481316255","id1488072475","id1492964317","id1519397914","id1519746792","id1531670603","id1533641021","id1544699237","id1560608260","id1563159261","id1565310917","id1092689152","com.beitakeji.zhipai","com.bettagames.wordbuddies","com.chaos.mergera","com.dragonmonster.idlefarmadventure.free","com.fillword.cross.wordmind.en","com.fotoable.mergetown","com.fotoable.MergicalHome","com.fotoable.NutsPoker","com.fotoable.palette","com.fotoable.townest","com.fotoable.villascrusher","com.fotoable.wordvilla.de","com.fotoable.WordVillas","com.island.card","com.jigsaw.wordplus","com.restaurant.rush.cookinggame.fever.frenzy","com.slots.free.vegas.casino.jackpotland","com.sports.real.disc.golf.online","com.sports.real.golf.rival.online","com.starfish.wordfrench.an","com.starfish.wordjp.an","com.tangramgames.gourddoll.wordcrush","com.tankgame.tankhero.en","com.wordfind.wortschau.de","com.wordgame.cross.android.en","com.wordgame.newcross.android.en","com.wordhome.newcross.android.en","com.fanatee.cody"]


def write_msg(data, file_path):
    with open(file_path, "a+") as f:
        f.write(data + "\n")


def add_bapp(read_file, write_file):
    with open(read_file, "r") as read:
        count = 0
        while True:
            line = read.readline()
            if not line:
                break
            try:
                data_dict = json.loads(line)
                if data_dict["black_white_info"]:
                    data_dict["black_white_info"]["b_app"] = bapp
                else:
                    data_dict["black_white_info"] = {"b_app": bapp}
                data_json = json.dumps(data_dict)
                write_msg(data_json, write_file)
                count += 1
            except Exception as e:
                print(e)
        print(count)


if __name__ == '__main__':
    add_bapp("/Users/mobvista/Downloads/merger_req.split-0", "/Users/mobvista/Downloads/merger_req.split-1")
