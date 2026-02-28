<script lang="ts">
	import { Button } from "$lib/components/ui/button";
	import * as Card from "$lib/components/ui/card";
</script>

<div class="min-h-screen flex flex-col">
	<!-- Navigation -->
	<header class="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
		<div class="container flex h-16 items-center justify-between px-4 md:px-8 max-w-7xl mx-auto">
			<div class="flex items-center gap-2">
				<img src="/projectflow-logo.svg" alt="ProjectFlow Logo" class="mt-2 h-32 w-64" />
			</div>
			<div class="flex items-center gap-4">
				<Button variant="ghost" href="/login">Log in</Button>
				<Button href="/register">Get Started</Button>
			</div>
		</div>
	</header>

	<main class="flex-1">
		<!-- Hero Section -->
		<section class="py-20 md:py-32 bg-linear-to-b from-background to-muted/20">
			<div class="container px-4 md:px-8 max-w-7xl mx-auto text-center">
				<h1 class="text-4xl font-extrabold tracking-tight sm:text-5xl md:text-6xl lg:text-7xl mb-6">
					AI-powered solution for <span class="text-primary">frontline workers</span>
				</h1>
				<p class="mx-auto max-w-(--desktop) text-muted-foreground md:text-xl mb-10">
					Meeting users where they are. We noticed that AI allows for more seamless use of software, 
					calling functions and performing calculations so your team doesn't have to.
				</p>
				<div class="flex flex-col sm:flex-row justify-center gap-4">
					<Button size="lg" href="/register" class="px-8 text-lg">Start Delegating</Button>
				</div>
			</div>
		</section>

		<!-- Features Grid -->
		<section class="py-20 bg-background">
			<div class="container px-4 md:px-8 max-w-7xl mx-auto">
				<div class="text-center mb-16">
					<h2 class="text-3xl font-bold tracking-tight sm:text-4xl mb-4">Focus on what affects users</h2>
					<p class="text-muted-foreground max-w-2xl mx-auto">
						We identified the core pillars of frontline success and built our tool to address them directly.
					</p>
				</div>
				<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
					<Card.Root>
						<Card.Header>
							<Card.Title>Communication</Card.Title>
							<Card.Description>Clarity for the whole group.</Card.Description>
						</Card.Header>
						<Card.Content>
							<p class="text-sm text-muted-foreground">
								Streamline team updates and ensure everyone is on the same page without the noise.
							</p>
						</Card.Content>
					</Card.Root>
					<Card.Root>
						<Card.Header>
							<Card.Title>Finances</Card.Title>
							<Card.Description>Automated clarity.</Card.Description>
						</Card.Header>
						<Card.Content>
							<p class="text-sm text-muted-foreground">
								Manual calculations are a thing of the past. AI handles the numbers while you handle the work.
							</p>
						</Card.Content>
					</Card.Root>
					<Card.Root>
						<Card.Header>
							<Card.Title>Knowledge Base</Card.Title>
							<Card.Description>Always accessible.</Card.Description>
						</Card.Header>
						<Card.Content>
							<p class="text-sm text-muted-foreground">
								Surface critical information instantly through our native AI integration.
							</p>
						</Card.Content>
					</Card.Root>
					<Card.Root>
						<Card.Header>
							<Card.Title>Usability</Card.Title>
							<Card.Description>Seamless integration.</Card.Description>
						</Card.Header>
						<Card.Content>
							<p class="text-sm text-muted-foreground">
								Instead of clicking around, let AI call functions and adjust settings for you.
							</p>
						</Card.Content>
					</Card.Root>
				</div>
			</div>
		</section>

		<!-- Gemini Highlight -->
		<section class="py-20 bg-muted/30">
			<div class="container px-4 md:px-8 max-w-7xl mx-auto">
				<div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
					<div>
						<h2 class="text-3xl font-bold tracking-tight sm:text-4xl mb-6">
							Powered by <span class="text-primary">Native Gemini Integration</span>
						</h2>
						<div class="space-y-4 text-muted-foreground md:text-lg">
							<p>
								Our project management tool leverages Gemini to help teams delegate tasks more effectively.
							</p>
							<p>
								The AI monitors workload across the team to ensure member burnout is prevented, 
								automatically suggesting reassignments when someone is overworked.
							</p>
							<p>
								Meet your team where they are, with software that adapts to their needs.
							</p>
						</div>
						<div class="mt-8">
							<Button href="/register">Experience AI Delegation</Button>
						</div>
					</div>
					<div class="relative aspect-video overflow-hidden rounded-xl border bg-background shadow-2xl flex items-center justify-center">
						<!-- Placeholder for a dashboard preview or AI animation -->
						<div class="text-center p-8">
							<div class="h-16 w-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
								<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-primary"><path d="M12 2a10 10 0 1 0 10 10H12V2Z"/><path d="M12 12 2.1 12.1"/><path d="m4.5 9.1 14.1 8.2"/><path d="m11.5 11.5 4-4"/><path d="m16 22-5-5"/></svg>
							</div>
							<h3 class="text-xl font-bold mb-2">Smart Dashboard</h3>
							<p class="text-sm text-muted-foreground">AI-driven task insights and team capacity monitoring.</p>
						</div>
					</div>
				</div>
			</div>
		</section>
	</main>

	<!-- Footer -->
	<footer class="border-t py-12 bg-background">
		<div class="container px-4 md:px-8 max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
			<div class="flex items-center gap-2">
				<img src="/projectflow-logo.svg" alt="ProjectFlow Logo" class="h-16 w-64 opacity-50" />
			</div>
			<p class="text-sm text-muted-foreground">
				© 2026 ProjectFlow. Built with ❤️ for the #swagathon.
			</p>
			<div class="flex gap-6">
				<a href="https://github.com/beaualbritton/project_manager" class="text-sm text-muted-foreground hover:text-foreground">GitHub</a>
			</div>
		</div>
	</footer>
</div>

<style>
	:global(html) {
		scroll-behavior: smooth;
	}
</style>
