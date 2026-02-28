<script lang="ts">
	import {
		NavigationMenuRoot,
		NavigationMenuContent,
		NavigationMenuItem,
		NavigationMenuLink,
		NavigationMenuList,
		NavigationMenuTrigger
	} from '$lib/components/ui/navigation-menu';
	import { logout } from '$lib/api/login';
  import { navigationMenuTriggerStyle } from "$lib/components/ui/navigation-menu/navigation-menu-trigger.svelte";

	async function handleLogout() {
		await logout();
    window.location.href = '/login';
	}
</script>
<div class="flex items-center w-full">
  <!-- Centered nav links -->
  <div class="flex-1 flex justify-center">
    <NavigationMenuRoot>
      <NavigationMenuList>
        <NavigationMenuItem>
            <NavigationMenuLink>
                {#snippet child()}
                    <a href="/dashboard" class={navigationMenuTriggerStyle()}>Dashboard</a>
                {/snippet}
            </NavigationMenuLink>
        </NavigationMenuItem>

        <NavigationMenuItem>
            <NavigationMenuLink>
                {#snippet child()}
                    <a href="/teams" class={navigationMenuTriggerStyle()}>Teams</a>
                {/snippet}
            </NavigationMenuLink>
        </NavigationMenuItem>

        <NavigationMenuItem>
            <NavigationMenuLink>
                {#snippet child()}
                    <a href="/tasks" class={navigationMenuTriggerStyle()}>Tasks</a>
                {/snippet}
            </NavigationMenuLink>
        </NavigationMenuItem>

        <NavigationMenuItem>
            <NavigationMenuLink>
                {#snippet child()}
                    <a href="/analytics" class={navigationMenuTriggerStyle()}>Analytics</a>
                {/snippet}
            </NavigationMenuLink>
        </NavigationMenuItem>
      </NavigationMenuList>
    </NavigationMenuRoot>
  </div>

  <!-- Right-aligned logout -->
  <NavigationMenuRoot>
    <NavigationMenuList>
      <NavigationMenuItem>
        <NavigationMenuLink>
          {#snippet child()}
              <button on:click={handleLogout} class={`${navigationMenuTriggerStyle()} text-red-500`}>
                Log out
              </button>
          {/snippet}
        </NavigationMenuLink>
      </NavigationMenuItem>
    </NavigationMenuList>
  </NavigationMenuRoot>
</div>
