# Raise the Nginx open file limit so it can serve many concurrent requests.
exec { 'fix--for-nginx':
  command => 'sed -i "s/15/4096/" /etc/default/nginx',
  path    => '/usr/local/bin/:/bin/',
}

# Restart Nginx so the new limit takes effect.
exec { 'nginx-restart':
  command => 'service nginx restart',
  path    => '/usr/local/bin/:/bin/:/usr/sbin/:/usr/bin/:/sbin/',
  require => Exec['fix--for-nginx'],
}
