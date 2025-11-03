import discord
from discord.ext import commands
from discord import app_commands
from typing import List


class RoleSelect(discord.ui.Select):
    """Dropdown menu for role selection"""
    
    def __init__(self):
        # Define the options for the dropdown
        options = [
            discord.SelectOption(
                label="Valorant Ranked",
                description="Get Valorant Ranked role",
                value="valorant_ranked"
            ),
            discord.SelectOption(
                label="Valorant Premier",
                description="Get Valorant Premier role",
                value="valorant_premier"
            ),
            discord.SelectOption(
                label="League of Legends",
                description="Get League of Legends role",
                value="lol"
            ),
            discord.SelectOption(
                label="Mmorpg",
                description="Get Mmorpg role",
                value="mmorpg"
            ),
            discord.SelectOption(
                label="Valheim",
                description="Get Valheim role",
                value="valheim"
            )
        ]
        
        super().__init__(
            placeholder="Select the games you want roles for...",
            min_values=0,  # Allow empty selection after Remove All
            max_values=len(options),  # Allow multiple selections
            options=options,
            custom_id="game_role_select"  # Add custom_id for persistence
        )

    async def callback(self, interaction: discord.Interaction):
        """Handle role selection"""
        
        # Defer the interaction first to avoid timeout
        await interaction.response.defer(ephemeral=True)
        
        # Define role mappings - you can customize these role names
        role_mappings = {
            "valorant_ranked": ["Valorant Ranked"],
            "valorant_premier": ["Valorant Premier"],
            "lol": ["League of Legends"],
            "mmorpg": ["Mmorpg"],
            "valheim": ["Valheim"]
        }
        
        # Get the guild (server)
        guild = interaction.guild
        if not guild:
            return
            
        # Get the member
        member = interaction.user
        if not isinstance(member, discord.Member):
            return
        
        # Get all possible game roles that this system manages
        all_managed_roles = []
        for role_list in role_mappings.values():
            all_managed_roles.extend(role_list)
        
        # Get roles that should be active based on current selection
        selected_role_names = []
        for game in self.values:
            if game in role_mappings:
                selected_role_names.extend(role_mappings[game])
        
        # If no values selected, user wants no roles (empty selection)
        if not self.values:
            selected_role_names = []
        
        # Collect roles to add and remove
        roles_to_add = []
        roles_to_remove = []
        
        # Process roles to add (selected but not currently held)
        for role_name in selected_role_names:
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                if role not in member.roles:
                    roles_to_add.append(role)
            else:
                # If role doesn't exist, create it
                try:
                    new_role = await guild.create_role(
                        name=role_name,
                        reason=f"Role created by {member.display_name} via /roles command"
                    )
                    roles_to_add.append(new_role)
                except discord.Forbidden:
                    return
                except Exception as e:
                    return
        
        # Process roles to remove (currently held but not selected)
        for role_name in all_managed_roles:
            if role_name not in selected_role_names:
                role = discord.utils.get(guild.roles, name=role_name)
                if role and role in member.roles:
                    roles_to_remove.append(role)
        
        # Process role changes
        response_parts = []
        
        # Add roles
        if roles_to_add:
            try:
                await member.add_roles(*roles_to_add, reason=f"Roles added via /roles command")
                role_names = [role.name for role in roles_to_add]
                if len(role_names) == 1:
                    response_parts.append(f"✅ Added role: **{role_names[0]}**")
                else:
                    response_parts.append(f"✅ Added roles: **{', '.join(role_names)}**")
                
            except discord.Forbidden:
                return
            except Exception as e:
                return
        
        # Remove roles (only those not selected)
        if roles_to_remove:
            try:
                await member.remove_roles(*roles_to_remove, reason=f"Roles removed via /roles command (not selected)")
                role_names = [role.name for role in roles_to_remove]
                if len(role_names) == 1:
                    response_parts.append(f"➖ Removed role: **{role_names[0]}**")
                else:
                    response_parts.append(f"➖ Removed roles: **{', '.join(role_names)}**")
                
            except discord.Forbidden:
                return
            except Exception as e:
                return
        
        # Process completed silently


class RoleView(discord.ui.View):
    """View containing the role selection dropdown"""
    
    def __init__(self):
        super().__init__(timeout=None)  # Persistent view
        self.add_item(RoleSelect())


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_messages = {}  # Store role message IDs per channel

    async def cog_load(self):
        """Called when the cog is loaded - restore persistent views"""
        # Add persistent view for existing role messages
        self.bot.add_view(RoleView())
    
    async def find_existing_role_messages(self):
        """Find and register existing role messages"""
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                try:
                    # Check if bot has permission to read message history
                    if not channel.permissions_for(guild.me).read_message_history:
                        continue
                        
                    # Search for role selection messages in this channel
                    async for message in channel.history(limit=50):
                        if (message.author == self.bot.user and 
                            message.embeds and 
                            len(message.embeds) > 0 and 
                            "Game Role Selection" in message.embeds[0].title):
                            # Found a role message, register it
                            self.role_messages[channel.id] = message.id
                            print(f"Found existing role message in #{channel.name} (ID: {message.id})")
                            break  # Only store the most recent one per channel
                except Exception as e:
                    # Skip channels we can't access
                    continue

    @app_commands.command(name="roles", description="Create a persistent role selection menu")
    async def roles(self, interaction: discord.Interaction):
        """Create a persistent role selection embed with dropdown"""
        
        # Check if user has manage roles permission
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message(
                "❌ You need 'Manage Roles' permission to use this command!", 
                ephemeral=True
            )
            return
        
        channel = interaction.channel
        
        # If this is the first time we're checking this channel, search for existing messages
        if channel.id not in self.role_messages:
            await self.find_existing_role_messages()
        
        # Check if there's already a role message in this channel
        existing_message = None
        if channel.id in self.role_messages:
            try:
                existing_message = await channel.fetch_message(self.role_messages[channel.id])
                print(f"Found tracked role message: {existing_message.id}")
            except discord.NotFound:
                # Message was deleted, remove from tracking
                print(f"Tracked role message was deleted, removing from tracking")
                del self.role_messages[channel.id]
                existing_message = None
            except Exception as e:
                print(f"Error fetching tracked message: {e}")
                existing_message = None
        
        # Create embed
        embed = discord.Embed(
            title="Game Role Selection",
            description="Select the games you play to get the corresponding roles!\n\n"
                       "**Available roles:**\n"
                       "**Valorant Ranked** - For Valorant ranked players\n"
                       "**Valorant Premier** - For Valorant premier players\n"
                       "**League of Legends** - For LoL players\n"
                       "**Mmorpg** - For MMORPG enthusiasts\n"
                       "**Valheim** - For Valheim players\n\n"
                       "**How to use:**\n"
                       "• Select the games you want roles for from the dropdown\n"
                       "• Your roles will match exactly what you select\n"
                       "• Select nothing in the dropdown to remove all roles\n"
                       "• Roles will be created automatically if they don't exist",
            color=0x5865F2
        )
        
        embed.set_footer(text="This menu will stay active permanently • Select your games below!")
        embed.set_thumbnail(url=interaction.guild.icon.url if interaction.guild.icon else None)
        
        # Create view with dropdown
        view = RoleView()
        
        if existing_message:
            # Update existing message
            try:
                await existing_message.edit(embed=embed, view=view)
                await interaction.response.send_message("✅ Role selection menu updated!", ephemeral=True)
            except Exception as e:
                # If failed to edit, send new message
                await interaction.response.send_message(embed=embed, view=view)
                message = await interaction.original_response()
                self.role_messages[channel.id] = message.id
        else:
            # Send new message
            await interaction.response.send_message(embed=embed, view=view)
            message = await interaction.original_response()
            self.role_messages[channel.id] = message.id

    @app_commands.command(name="roles-remove", description="Remove specific game roles from yourself")
    @app_commands.describe(
        role_name="The name of the role to remove (e.g., 'Valorant', 'League of Legends')"
    )
    async def roles_remove(self, interaction: discord.Interaction, role_name: str):
        """Remove a specific role from the user"""
        
        guild = interaction.guild
        member = interaction.user
        
        if not guild or not isinstance(member, discord.Member):
            await interaction.response.send_message("❌ This command can only be used in a server!", ephemeral=True)
            return
        
        # Find the role
        role = discord.utils.get(guild.roles, name=role_name)
        if not role:
            await interaction.response.send_message(f"❌ Role '{role_name}' not found!", ephemeral=True)
            return
        
        # Check if user has the role
        if role not in member.roles:
            await interaction.response.send_message(f"❌ You don't have the '{role_name}' role!", ephemeral=True)
            return
        
        # Remove the role
        try:
            await member.remove_roles(role, reason=f"Role removed via /roles-remove command")
            await interaction.response.send_message(f"✅ Removed role: **{role_name}**", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to remove roles!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error removing role: {str(e)}", ephemeral=True)

    @app_commands.command(name="roles-list", description="List all available game roles")
    async def roles_list(self, interaction: discord.Interaction):
        """List all available game roles in the server"""
        
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("❌ This command can only be used in a server!", ephemeral=True)
            return
        
        # Game roles to look for
        game_roles = ["Valorant Ranked", "Valorant Premier", "League of Legends", "Mmorpg", "Valheim"]
        
        embed = discord.Embed(
            title="Available Game Roles",
            description="Here are all the game roles available in this server:",
            color=0x5865F2
        )
        
        found_roles = []
        missing_roles = []
        
        for role_name in game_roles:
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                member_count = len(role.members)
                found_roles.append(f"• **{role_name}** - {member_count} member{'s' if member_count != 1 else ''}")
            else:
                missing_roles.append(f"• **{role_name}** - Not created yet")
        
        if found_roles:
            embed.add_field(
                name="✅ Existing Roles",
                value="\n".join(found_roles),
                inline=False
            )
        
        if missing_roles:
            embed.add_field(
                name="➕ Available to Create",
                value="\n".join(missing_roles),
                inline=False
            )
        
        embed.set_footer(text="Use /roles to get roles or create missing ones!")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="roles-cleanup", description="Remove old role selection messages from this channel")
    async def roles_cleanup(self, interaction: discord.Interaction):
        """Clean up old role selection messages"""
        
        # Check if user has manage messages permission
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                "❌ You need 'Manage Messages' permission to use this command!", 
                ephemeral=True
            )
            return
        
        channel = interaction.channel
        deleted_count = 0
        
        # Search for role selection messages
        async for message in channel.history(limit=100):
            if (message.author == self.bot.user and 
                message.embeds and 
                len(message.embeds) > 0 and 
                "Game Role Selection" in message.embeds[0].title):
                try:
                    await message.delete()
                    deleted_count += 1
                except Exception:
                    pass
        
        # Clear tracking for this channel
        if channel.id in self.role_messages:
            del self.role_messages[channel.id]
        
        if deleted_count > 0:
            await interaction.response.send_message(
                f"✅ Removed {deleted_count} old role selection message{'s' if deleted_count != 1 else ''}!", 
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "ℹ️ No role selection messages found to remove.", 
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(Roles(bot))