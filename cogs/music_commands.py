import logging

import disnake
from disnake.ext import commands
from yt_dlp import YoutubeDL

from exceptions import APIException


class Music(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.is_playing: bool = False
        self.is_paused: bool = False
        self.music_queue: list = []
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
            }
        self.YDL_OPTIONS = {
            'format': 'bestaudio',
            'noplaylist': 'true',
            }
        self.vc = None

    @commands.Cog.listener()
    async def on_ready(self):
        print('Music cog loaded.')

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info('ytsearch:%s' % item, download=False)['entries'][0]
            except Exception:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)
            player = disnake.FFmpegPCMAudio(source=m_url,
                                            **self.FFMPEG_OPTIONS)
            self.vc.play(
                player,
                after=lambda e: self.play_next()
                )
        else:
            self.is_playing = False
    
    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            if self.vc is None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()
                if self.vc is None:
                    await ctx.send(content='Не удалось подключиться к голосовому каналу.')
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            self.music_queue.pop(0)
            player = disnake.FFmpegPCMAudio(source=m_url,
                                            **self.FFMPEG_OPTIONS)
            self.vc.play(
                player,
                after=lambda e: self.play_next()
                )
        else:
            self.is_playing = False
        
    @commands.command(name='play',
                      description='Play music.',)
    async def play(self, ctx,
                   *args
                   ) -> None:
        query = ' '.join(args)
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send('Вы не находитесь в канале.')
        elif len(self.music_queue) == 0 and query == '':
            await ctx.send('Нечего проигрывать.')
        elif self.music_queue is not None and query == '':
            if self.is_playing is False:
                await ctx.send('Запускаю.')
                await self.play_music(ctx)
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if not isinstance(bool, song):
                await ctx.send('Что-то пошло не так!')
            else:
                await ctx.send('Трек добавлен в очередь.')
                self.music_queue.append([song, voice_channel])
                if self.is_playing is False:
                    await self.play_music(ctx)
    
    @commands.command(name='pause',
                      description='Pause music.')
    async def pause(self, ctx) -> None:
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()
    
    @commands.command(name='resume',
                      description='Resume music.')
    async def resume(self, ctx) -> None:
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()

    @commands.command(name='skip',
                      description='Skip track.')
    async def skip(self, ctx) -> None:
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)
    
    @commands.command(name='clear_queue',
                      description='Clear all songs.')
    async def clear(self, ctx) -> None:
        if self.vc is not None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send('Очередь была очищена.')

    @commands.command(name='leave',
                      description='Leave the voice channel.')
    async def leave(self, ctx) -> None:
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()
        

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Music(bot))