import discord
import requests
import json
from discord.ext import commands
from bs4 import BeautifulSoup


class Jsontools:
    def __init__(self):
        self.json_file = r'runes.json'

    def json_open(self):
        with open(self.json_file, 'r') as f:
            read_file = f.read()
            json_load = json.loads(read_file)
        return json_load

    def rune_to_id(self, name):
        json_file = self.json_open()
        if name in json_file:
            return json_file[name]


class Runes:
    def __init__(self, client, ctx, champion):
        self.url = 'https://u.gg/lol/champions/'
        self.client = client
        self.ctx = ctx
        self.champion = champion
        self.new_url = self.champion_url()
        self.jt = Jsontools()

    def champion_url(self):
        url = self.url + f'{self.champion}/build'
        result = requests.get(url)
        doc = BeautifulSoup(result.text, 'html.parser')
        rec_build = doc.find(class_='champion-profile-main-page')
        return rec_build  # returns recommended build

    def keystone(self):
        primary_runes = self.new_url.find(class_='primary-tree')
        selected_rune = primary_runes.find(class_='perk keystone perk-active')
        keystone_name = selected_rune.find('img')['alt'][13:]
        keystone_id = self.jt.rune_to_id(keystone_name)
        return keystone_name, keystone_id

    def primary_runes(self):
        primary_perks = self.new_url.find(class_='primary-tree')
        selected_perks = primary_perks.find_all(class_='perk perk-active')
        perks_list = [perks.find('img')['alt'][9:] for perks in selected_perks]
        perks1 = self.jt.rune_to_id(perks_list[0])
        perks2 = self.jt.rune_to_id(perks_list[1])
        perks3 = self.jt.rune_to_id(perks_list[2])
        return perks_list[0], perks_list[1], perks_list[2], perks1, perks2, perks3

    def secondary_runes(self):
        primary_perks = self.new_url.find(class_='secondary-tree')
        selected_perks = primary_perks.find_all(class_='perk perk-active')
        perks_list = [perks.find('img')['alt'][9:] for perks in selected_perks]
        perks1 = self.jt.rune_to_id(perks_list[0])
        perks2 = self.jt.rune_to_id(perks_list[1])
        return perks_list[0], perks_list[1], perks1, perks2

    def shards(self):
        shards = self.new_url.find(
            class_='rune-tree_v2 stat-shards-container_v2')
        selected_shards = shards.find_all(class_='shard shard-active')
        shards_list = [shards.find('img')['alt'][4:]
                       for shards in selected_shards]
        shards1 = self.jt.rune_to_id(shards_list[0])
        shards2 = self.jt.rune_to_id(shards_list[1])
        shards3 = self.jt.rune_to_id(shards_list[2])
        return shards_list[0], shards_list[1], shards_list[2], shards1, shards2, shards3

    def summoner_spells(self):
        spells_list = []
        summ_spells = self.new_url.find(class_='summoner-spells')
        spells = summ_spells.find_all('img')
        for i in range(2):
            spells_list.append(spells[i]['alt'][15:])
        spells1 = self.jt.rune_to_id(spells_list[0])
        spells2 = self.jt.rune_to_id(spells_list[1])
        return spells_list[0], spells_list[1], spells1, spells2

    def icons(self):
        tree_icons = self.new_url.find_all(class_='rune-image-container')
        champion_icon = self.new_url.find(class_='champion-image-border')

        primary_tree = tree_icons[0].find('img')['alt'][14:]
        secondary_tree = tree_icons[1].find('img')['alt'][14:]

        primary_tree_icon = self.jt.rune_to_id(primary_tree)
        secondary_tree_icon = self.jt.rune_to_id(secondary_tree)
        champ_icon = champion_icon.find('img')['src']

        primary_tree_url = tree_icons[0].find('img')['src']
        return primary_tree, secondary_tree, primary_tree_icon, secondary_tree_icon, champ_icon, primary_tree_url

    def winrate(self):
        winrate_info = self.new_url.find(class_='wr-matches')
        winrate = winrate_info.find_all('span')
        wr = winrate[0].string
        matches = winrate[1].string
        return wr, matches

    def embed_format(self):
        keystone_name, keystone_id = self.keystone()
        shards = self.shards()
        summs = self.summoner_spells()
        primary_perks = self.primary_runes()
        secondary_perks = self.secondary_runes()
        icons = self.icons()
        winrate = self.winrate()

        keystone_icon = self.client.get_emoji(keystone_id)
        summs1_icon = self.client.get_emoji(summs[2])
        summs2_icon = self.client.get_emoji(summs[3])
        shards1_icon = self.client.get_emoji(shards[3])
        shards2_icon = self.client.get_emoji(shards[4])
        shards3_icon = self.client.get_emoji(shards[5])
        primary_perks1_icon = self.client.get_emoji(primary_perks[3])
        primary_perks2_icon = self.client.get_emoji(primary_perks[4])
        primary_perks3_icon = self.client.get_emoji(primary_perks[5])
        secondary_perks1_icon = self.client.get_emoji(secondary_perks[2])
        secondary_perks2_icon = self.client.get_emoji(secondary_perks[3])
        secondary_tree_icon = self.client.get_emoji(icons[3])

        embed = discord.Embed(
            colour=discord.Colour.blue(),
        )
        embed.set_author(
            name=f'{icons[0].upper()} [PRIMARY TREE]', icon_url=icons[5])
        embed.set_thumbnail(url=icons[4])
        embed.set_footer(text=f'{winrate[0]}{winrate[1]}', icon_url=icons[4])

        embed.add_field(
            name='Summoner Spells', value=f'{summs1_icon}{summs[0]} {summs2_icon}{summs[1]}', inline=True)
        embed.add_field(
            name='\u200b', value=f'**{keystone_icon} {keystone_name}**', inline=False)
        embed.add_field(
            name='\u200b', value=f'{primary_perks1_icon} {primary_perks[0]}', inline=False)
        embed.add_field(
            name='\u200b', value=f'{primary_perks2_icon} {primary_perks[1]}', inline=False)
        embed.add_field(
            name='\u200b', value=f'{primary_perks3_icon} {primary_perks[2]}', inline=False)

        embed.add_field(
            name='\u200b', value=f'**{secondary_tree_icon} {icons[1].upper()} [SECONDARY TREE]**', inline=False)
        embed.add_field(
            name='\u200b', value=f'{secondary_perks1_icon} {secondary_perks[0]}', inline=False)
        embed.add_field(
            name='\u200b', value=f'{secondary_perks2_icon} {secondary_perks[1]}', inline=False)

        embed.add_field(
            name='\u200b', value=f'{shards1_icon} {shards[0][:-5]}/{shards2_icon} {shards[1][:-5]}/{shards3_icon} {shards[2][:-5]}', inline=False)

        return embed

    async def main(self):
        embed = self.embed_format()
        await self.ctx.send(embed=embed)


class RunesCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def runes(self, ctx, arg):
        await Runes(self.client, ctx, arg).main()


def setup(client):
    client.add_cog(RunesCommands(client))
    print('[runes.py] loaded')
