---
title: "Stripping surveillance parameters from Facebook and Google links"
date: 2020-10-16T06:32:53-04:00
draft: false
authorbox: false
sidebar: false
tags:
- perl
- privacy
- facebook
- google
categories:
- programming
---
While largely opaque to most users, Facebook and Google massage any links that you acquire on their sites to include data used to track you around the web. This script attempts to strip these surveillance parameters from the URL's. It is by no means all-inclusive. Imaginably, there are links that I haven't yet encountered and that need to be considered in a future version. So consider this a proof-of-concept.

### The problem

For example, I performed a Google search[^1] for "Smarties". Inspecting the first link - to Wikipedia, I see:

```https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjsjeW35LjsAhXuYt8KHSuLCbsQFjAAegQIARAC&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FSmarties&usg=AOvVaw1fpahjjexXarc2XibGIA91```

What is all this garbage? Just give me the Wikipedia link.

Similarly, with Facebook, here's a representative link from a post shared by a friend:

```https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.propublica.org%2Farticle%2Finside-the-fall-of-the-cdc%2Famp%3F__twitter_impression%3Dtrue%26fbclid%3DIwAR1vPirl6QnkEg_3alUgWAeKUnJNtg-Yt_A2p-xzAksE8wa8ehJ0J702fDs&h=AT1abE7Jz5DjxA_jpN_8Ak5JB4oMSxFJLchizp-UlJgNPI9n0iXDb513sIAZ3uV1gHCazWY92umXONwvxHWZyDK7AFp29zy4W9ifzU6XJC9gdsvhjsY_GgW6-d1TwfV1NTpj5IqutA&__tn__=H-R&c[0]=AT0wPBsJAwDQs1I3A-IE7zqQqBiwEHA3kJW9oLxfh04m_WvjBdWOcmz-6vYfoSNsdLLYxRWgAKZw3ExnMZ2CUH-0nRSmILzqTmumL68oL5-OcChT8pbK11VBSHVG1nt64-Ek8S1AESqn8nYCjZ-gI80uo3Hhd8UJyvOD-KoZ3yI_M5Gfcdu1```

Again, garbage that exists only so that Facebook can follow me around the web and generate behavioural data that they can use in turn against my better interests and those of society at large.

After the sanitization process below, we have:

```https://www.propublica.org/article/inside-the-fall-of-the-cdc/amp```

Nice and tidy with only what is needed to route me to the desired link without unnecessary tracking data.

### Solution

The solution is to strip out the cruft with which surveillance capitalists corrupt the web. I've applied this script as a Keyboard Maestro but it could be reconfigured with ease as a macOS text service. Or the same idea could be implemented in other OS flavours.

{{< highlight perl >}}
#!/usr/bin/perl

sub urldecode {
    my ($rv) = @_;
    $rv =~ s/\+/ /g;
    $rv =~ s/%(..)/pack("c",hex($1))/ge;
    return $rv;
}

sub urlencode {
    my ($rv) = @_;
    $rv =~ s/([^A-Za-z0-9])/sprintf("%%%2.2X", ord($1))/ge;
    return $rv;
}

# remove referral parameters
sub strip_utm {
    $_ = shift @_;
    s/(.*[?]?)utm_source=facebook&?(.*)/$1$2/g;
    s/(.*)(utm_medium=.*?)&(.*)/$1$3/g;
    s/(.*)(utm_campaign=.*?)&(.*)/$1$3/g;
    s/(.*)(utm_brand=.*?)&(.*)/$1$3/g;
    s/(.*)(utm_social-type=.*?)&(.*)/$1$3/g;
    s/^(.*)(fbclid=[^\&]*)(.*)$/$1$3/g;
    s/^(.*)(h=[^\&]*)(.*)$/$1$3/g;
    s/^(.*)(__tn__=[^\&]*)(.*)$/$1$3/g;
    s/^(.*)([A-Za-z]\[\d+\]=[^\&]*)(.*)$/$1$3/g;
    s/(.*)(__twitter_impression=[^&]+)/$1/g;
    # eliminate duplicate & from the stripping process
    s/&+/&/g;
    # clean up
    s/^(.*)\?+\&+$/$1/g;
    return $_;
}

my $original_url = $ARGV[0];
# my $original_url = $ENV{KMVAR_unsterile_link};

# decode the url as needed
my $url_text = ($original_url =~ m/%3A/) ? urldecode($original_url) : $original_url;
# fix links from Facebook
if ( $url_text =~ m/l\.facebook\.com/ ) {
    # strip the actual link
    $url_text =~ m/http[s]?.*l.facebook.*?u=(.*)/;
    print strip_utm($1);
}
else {
    $_ = $url_text;
    # deal with google referrals
    if( m/http[s]?:.*google\.com\/url\?/ ) {
        s/url=([^&]*)/$1/g;
        print $1;
    }
    else {
        strip_utm($_);
        print $_;
    }
}
{{< /highlight >}}

### Next steps

- **Strip Amazon referral links** - yes, I know some people monetize their blogs in whole or in part using Amazon referral links. I don't care. If bloggers want to make money that way, then develop relationships with smaller commercial entities, those that support and live in their local communities and treat their employees with dignity.
- **Strip Twitter links** - Deal with links from the seething cauldron of hate and incivility that is Twitter.

[^1]: Ordinarily I don't use Google services at all, even for search. But I did for this example.