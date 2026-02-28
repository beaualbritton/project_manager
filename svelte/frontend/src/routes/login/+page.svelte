<!-- src/routes/login/+page.svelte -->
<script lang="ts">
  import { Button } from '$lib/components/ui/button';
  import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '$lib/components/ui/card';
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
          <CardTitle class="text-2xl">Login</CardTitle>
          <CardDescription>Enter your username and password below to login to your account</CardDescription>
        </CardHeader>
        <CardContent>
          <form method="POST" class="grid gap-4">
            {#if form?.error}
              <p class="text-sm text-red-500">{form.error}</p>
            {/if}
            <div class="grid gap-2">
              <Label for="username">Username</Label>
              <Input id="username" name="username" type="text" placeholder="username" required />
            </div>
            <div class="grid gap-2">
              <Label for="password">Password</Label>
              <Input id="password" name="password" type="password" required />
            </div>
            <Button type="submit" class="w-full">Login</Button>
          </form>
        </CardContent>
        <CardFooter>
          <div class="mt-4 text-center text-sm">
            Don't have an account?
            <a href="/register" class="underline">Sign up</a>
          </div>
        </CardFooter>
      </Card>
    </div>
  </div>
</div>
