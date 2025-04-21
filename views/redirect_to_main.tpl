<%inherit file='base.tpl'/>
<%block name="content">

<div id="redirect_to_main_container">
    <h2>{{!message}} Redirecting you back to the main landing page in 5 seconds...</h2>
</div>

<script>
    setTimeout(function() {
        window.location.href = "/";
    }, 5000);
</script>

</%block>
