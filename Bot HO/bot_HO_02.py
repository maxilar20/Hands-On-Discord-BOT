# -*- coding: utf-8 -*-
import os
import random
import discord
import csv
import json
import pandas as pd



TOKEN = 'NzI0MzU1NTk2MTc4MDMwNTkz.Xu--uA.pFanicbeo2KMFK46DLA_4hrzqYw'
GUILD = 'Hands-On RD'

client = discord.Client()

async def update_player(member, name, level, casa, coh=0):
    # Changing nickname
    await member.edit(nick=name)

    # Assigning rols
    rol_level = discord.utils.get(member.guild.roles, name=level)
    if str(coh) == '1':
        rol_coh = discord.utils.get(member.guild.roles, name="COH")
        await member.edit(roles=[rol_level, rol_coh])
    else:
        rol_casa = discord.utils.get(member.guild.roles, name=casa)
        await member.edit(roles=[rol_casa, rol_level])

def read_discord_id():
    with open('test.csv') as doc:
        reader = csv.reader(doc)
        discord_ids = {}
        for idx, row in enumerate(reader):
            if idx == 0:
                cols = row
            else:
                ID = row[0].lower()
                discord_ids[ID] = row[1]
    return discord_ids

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )
    print('Guild Members:')
    for member in guild.members:
        print(member.name.encode('utf-8'))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(message.channel)
    mensaje = message.content
    mensaje = mensaje.lower()


    if mensaje.startswith('reglas'):
        await message.channel.send('One player clicks the button below and reads the prompt to everyone. \n One by one, the reader and the other players cast a voice vote for which other player BEST matches that description. Nobody can vote for the reader this round. \n The player who gets the most votes is crowned Monarch of Lineup, gets to read the next prompt, and is immune for that round. \n In case of a tie vote, everyone is quarantined to their own home indefinitely.\n The winner is everyone who’s still friends at the end of all this.')

    if mensaje.startswith('voto'):
        nombre = mensaje.strip('voto ')
        nombre = nombre.title()
        if nombre not in votos:
            votos[nombre] = 1
        else:
            votos[nombre] = votos[nombre] + 1

        msg_voto = str(nombre) + ' tiene ' + str(votos[nombre]) + ' votos'
        await message.channel.send(msg_voto)

    if mensaje.startswith('resultados'):
        for key in votos:
            if votos[key] != 0:
                msg_resultados = str(key) + ' tiene ' + str(votos[key]) + ' votos'
                await message.channel.send(msg_resultados)

    if str(message.channel) == "activacion":
        await message.delete()
        id = int(mensaje)
        print(id)

        # ID found in xlsx file
        with open('DataBase_prueba.xlsx', 'rb') as file :
            players = pd.read_excel(file, sheet_name='players', index_col=0, header=0)
        #print(players)
        if id in players.index:
            nombre = str(players.loc[id]['nombre']).title()
            puntos = int(players.loc[id]['puntos'])
            #level = str(players.loc[id]['rango'])
            level = "Blanco"
            equipo = str(players.loc[id]['equipo_actual'])
            casa = str(players.loc[id]['casa'])
            coh = int(players.loc[id]['coh'])

            await message.channel.send("Hola " + nombre  + ", estas en el equipo " + equipo + " y perteneces a la casa " + casa, delete_after=5)
            print("Hola " + nombre  + ", estas en el equipo " + equipo + " y perteneces a la casa " + casa)

            member = message.author
            await update_player(member,nombre, level, casa, coh)

            data = {id : member.id}
            with open("./discordid/" + str(id) + ".json", "w") as write_file:
                json.dump(data, write_file)

        else:
            # No id found
            await message.channel.send("El id " + str(id) + " no existe", delete_after=5)


    if str(message.channel) == "chat-coh":
        if mensaje == '!update':
            with open('DataBase_prueba.xlsx', 'rb') as file :
                players = pd.read_excel(file, sheet_name='players', index_col=0, header=0)

            discord_ids = read_discord_id()
            #for id in discord_ids:
            await message.channel.send("Procesando...")
            for id in discord_ids:
                print(id)
                id = int(id)
                nombre = str(players.loc[id]['nombre']).title()
                nombre = nombre[:32] if len(nombre) > 32 else nombre
                puntos = int(players.loc[id]['puntos'])
                #level = str(players.loc[id]['rango'])
                level = "Blanco"
                equipo = str(players.loc[id]['equipo_actual'])
                casa = str(players.loc[id]['casa'])
                coh = int(players.loc[id]['coh'])
                discord_id = discord_ids[str(id)]
                member = message.guild.get_member(int(discord_id))
                await update_player(member,nombre, level, casa, coh)

            await message.channel.send("Terminado")



client.run(TOKEN)
