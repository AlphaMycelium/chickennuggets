import logging
import traceback

import discord

from chickennuggets.footer import set_footer


ERROR_COLOR = discord.Color.from_rgb(255, 0, 0)

logger = logging.getLogger(__name__)


async def process_unknown_error(ctx, error):
    """
    Handle another, unknown exception by sending it to the bot owner.

    Forward the error message to the bot's owner, and send a generic message
    to the command author with an apology.
    """

    # Get traceback message
    trace = ''.join(traceback.format_exception(
        type(error), error, error.__traceback__))
    # Add to logs
    logger.error(trace)

    # Apologise to command author
    logger.info('Apologising to command author')

    embed = discord.Embed(
        title='Unknown Error',
        description=(
            f'An error has occured in {ctx.bot.user.name}. I\'m sorry. '
            'Details of the problem have been sent to my creator.'
        ),
        color=ERROR_COLOR
    )
    set_footer(embed)
    await ctx.author.send(embed=embed)

    # Build an embed with exception details
    embed = discord.Embed(
        title='Unhandled Exception',
        description=f'```{trace}```',
        color=ERROR_COLOR
    )
    embed.add_field(
        name='Command',
        value=ctx.message.content
    )
    set_footer(embed)

    # Send to bot owner for analysis
    appinfo = await ctx.bot.application_info()
    await appinfo.owner.send(embed=embed)

    logger.info('Sent unhandled error to bot owner')