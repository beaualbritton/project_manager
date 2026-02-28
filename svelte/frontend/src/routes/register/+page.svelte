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
	export let form;
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
					<CardTitle class="text-2xl">Register</CardTitle>
					<CardDescription>Enter your details to create an account</CardDescription>
				</CardHeader>
				<CardContent>
					<form method="POST" action="?/register" class="grid gap-4">
						<div class="grid gap-2">
							<Label for="username">Username</Label>
							<Input id="username" name="username" required />
						</div>
						<div class="grid gap-2">
							<Label for="email">Email</Label>
							<Input id="email" name="email" type="email" placeholder="m@example.com" required />
						</div>
						<div class="grid gap-2">
							<Label for="password">Password</Label>
							<Input id="password" name="password" type="password" required />
						</div>
						<div class="grid gap-2">
							<Label for="companyId">Company ID</Label>
							<Input id="companyId" name="companyId" required />
						</div>
						<Button type="submit" class="w-full">Create an account</Button>
					</form>
				</CardContent>
				<CardFooter>
					<div class="mt-4 text-center text-sm">
						Already have an account?
						<a href="/login" class="underline"> Sign in </a>
					</div>
				</CardFooter>
			</Card>
		</div>
	</div>
</div>
