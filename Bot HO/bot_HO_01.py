# -*- coding: utf-8 -*-
import os
import random
import discord
import csv
import json



TOKEN = 'NzI0MzU1NTk2MTc4MDMwNTkz.Xu--uA.pFanicbeo2KMFK46DLA_4hrzqYw'
GUILD = 'Hands-On RD'

client = discord.Client()


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
        id = mensaje

        with open('usuarios_4.csv') as doc:
            reader = csv.reader(doc)
            result = {}
            for idx, row in enumerate(reader):
                if idx == 0:
                    cols = row
                else:
                    ID = row[0].lower()
                    result[ID] = row[1:]

        # ID found in csv file
        if id in result:
            nombre = result[id][0]
            puntos = result[id][1]
            level = result[id][2]
            equipo = result[id][3]
            casa = result[id][4]
            coh = result[id][5]

            await message.channel.send("Hola " + nombre  + ", estas en el equipo " + equipo + " y perteneces a la casa " + casa, delete_after=5)
            print("Hola " + nombre  + ", estas en el equipo " + equipo + " y perteneces a la casa " + casa)
            print(id)

            user = message.author
            rol_casa = discord.utils.get(message.guild.roles, name=casa)
            rol_level = discord.utils.get(message.guild.roles, name=level)
            rol_coh = discord.utils.get(message.guild.roles, name="COH")

            data = {id : user.id}
            with open("./discordid/" + id + ".json", "w") as write_file:
                json.dump(data, write_file)

            # Changing nickname
            await user.edit(nick=nombre)

            # Assigning rols
            if str(coh) == '1':
                await user.edit(roles=[rol_level, rol_coh])
            else:
                await user.edit(roles=[rol_casa, rol_level])

        else:
            # No id found
            await message.channel.send("El id " + id + " no existe", delete_after=5)

client.run(TOKEN)
