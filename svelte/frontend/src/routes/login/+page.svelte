<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import {
		Card,
		CardContent,
		CardDescription,
		CardFooter,
		CardHeader,
		CardTitle
	} from '$lib/components/ui/card';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
</script>

<div class="w-full lg:grid lg:min-h-[600px] lg:grid-cols-2 xl:min-h-[800px]">
	<div class="hidden bg-muted lg:block">
		<div class="flex flex-col justify-center items-center h-full">
			<img src="/projectflow-logo.svg" alt="ProjectFlow" class="mt-2" />
		</div>
	</div>
	<div class="flex items-center justify-center py-12">
		<div class="mx-auto grid w-[350px] gap-6">
			<Card>
				<CardHeader>
					<CardTitle class="text-2xl">Login</CardTitle>
					<CardDescription>Enter your username and password below to login to your account</CardDescription>
				</CardHeader>
				<CardContent>
					<div class="grid gap-4">
						<div class="grid gap-2">
							<Label for="username">Username</Label>
							<Input id="username" type="text" placeholder="m@example.com" required />
						</div>
						<div class="grid gap-2">
							<div class="flex items-center">
								<Label for="password">Password</Label>
							</div>
							<Input id="password" type="password" required />
						</div>
						<Button type="submit" class="w-full">Login</Button>
					</div>
				</CardContent>
				<CardFooter>
					<div class="mt-4 text-center text-sm">
						Don&apos;t have an account?
						<a href="/register" class="underline"> Sign up </a>
					</div>
				</CardFooter>
			</Card>
		</div>
	</div>
</div>
