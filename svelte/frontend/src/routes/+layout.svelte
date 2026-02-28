<script lang="ts">
	import { page } from '$app/stores';
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import Nav from '$lib/components/nav.svelte';

	let { children } = $props();
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>
{#if $page.url.pathname !== '/login' && $page.url.pathname !== '/register'}
	<Nav />
{/if}
{@render children()}
