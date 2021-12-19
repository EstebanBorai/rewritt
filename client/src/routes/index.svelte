<script lang="ts">
	let file;
	let isLoading = false;
	let downloadLink = null;

	async function showFile(blob) {
		const file = new Blob([blob], { type: 'application/pdf' });
		const data = window.URL.createObjectURL(file);

		downloadLink = {
			href: data
		};
	}

	async function submit(event) {
		try {
			isLoading = true;
			event.preventDefault();

			const fileInput = document.getElementById('file_input');
			const form = new FormData();

			form.append('file', fileInput.files[0]);

			const response = await fetch('http://0.0.0.0:5000/api/v1/convert', {
				method: 'POST',
				body: form
			});

			const blob = await response.blob();

			showFile(blob);
		} catch (error) {
		} finally {
			isLoading = false;
		}
	}
</script>

{#if isLoading}
	<h1>Loading...</h1>
{:else if downloadLink}
	<a href={downloadLink.href} download="file.pdf">Download</a>
{:else}
	<form on:submit={submit}>
		<input type="file" name="file" bind:value={file} id="file_input" />
		<input type="submit" value="Upload" />
	</form>
{/if}
