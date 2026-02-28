<script lang="ts">
import { logout } from "$lib/api/login";
import WrapperButton from "$lib/components/wrapper_button.svelte";
async function logoutSubmit()
{
  let response = await logout();
}
</script>

<main>
  <div>
  <WrapperButton title="logout" toggle={logout}/>
  </div>

</main>
