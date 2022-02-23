% rebase("base.tpl", title=title)

<h2>{{!message}} Redirecting you back to the main landing page in 5 seconds...</h2>

<script>
    setTimeout(function() {
        window.location.href = "/";
    }, 5000);
</script>
