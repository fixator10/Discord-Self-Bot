import asyncio
import json

from discord.ext import commands

tag_location = "data/SelfBot/tags.json"


class Tags:
    def __init__(self, bot):
        self.bot = bot

        try:
            with open(tag_location) as f:
                try:
                    self.tags = json.load(f)
                # if file is heck
                except json.JSONDecodeError:
                    self.create_tags()
        except FileNotFoundError:
            self.create_tags()

        asyncio.Task(self.save_tags())

    def create_tags(self):
        save = "{}"
        with open(tag_location, "w") as f:
            f.write(save)
        with open(tag_location) as f:
            self.tags = json.load(f)

    @commands.command(pass_context=True)
    async def rmtag(self, ctx, command: str):
        """Removes a tag
        Usage:
        self.rmtag tag"""
        command = command.lower()
        if command in self.tags:
            del self.tags[command]
            await self.bot.say("Tag {} has been removed :thumbsup:".format(command))
        else:
            await self.bot.say("Tag not registered, could not delete :thumbsdown: ")

    @commands.command(pass_context=True, name="tags")
    async def _tags(self, ctx):
        """Lists the tags added
        Usage:
        self.tags"""
        taglist = "```diff\nTags:"
        for x in self.tags.keys():
            taglist = "{}\n- {}".format(taglist, x)
        await self.bot.say("{0} ```".format(taglist))

    @commands.command(pass_context=True)
    async def tag(self, ctx, userinput: str, *, output: str = None):
        """Adds or displays a tag
        Usage:
        self.tag tag_name tag_data
        If 'tag_name' is a saved tag it will display that, else it will
        create a new tag using 'tag_data'"""
        userinput = userinput.lower()
        if userinput in self.tags:
            await self.bot.say(self.tags[userinput])
        else:
            if output is not None:
                self.tags[userinput] = output
                if output.startswith("http"):
                    await self.bot.say("Tag {} has been added with output <{}> :thumbsup:".format(userinput, output))
                else:
                    await self.bot.say("Tag {} has been added with output {} :thumbsup:".format(userinput, output))

    async def save_tags(self):
        while True:
            save = json.dumps(self.tags)
            with open(tag_location, "w") as data:
                data.write(save)
            await asyncio.sleep(60)


def setup(bot):
    bot.add_cog(Tags(bot))
