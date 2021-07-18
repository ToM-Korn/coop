# coop
buying syndicate platform


# for deployment
## static files for admin templates 

first create a folder "static" in your root folder

in terminal use: "python manage.py collectstatic" to collect the admin interface static files to your static folder including admin templates


## lighttp config
my currently working config looks like:

    $HTTP["host"] == "example.com" {
        server.document-root = "/var/www/coop"
        $HTTP["url"] !~ "^/static" {
        fastcgi.server = ("/" => (
                "food" => (
                "socket" => "/tmp/fastcgi-coop.python.socket",
                "bin-path" => "/var/www/coop/fcgi.py",
                "check-local" => "disable",
                "fix-root-scriptname" => "enable",
                "max-procs" => 1,
                )
        ),
        )}
    }


