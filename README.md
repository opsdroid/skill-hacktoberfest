# opsdroid skill hacktoberfest

A skill for [opsdroid](https://github.com/opsdroid/opsdroid) to comment [Hacktoberfest](https://hacktoberfest.digitalocean.com/) messages on new PRs.

## Requirements

You must have the GitHub connector configured.

## Configuration

You must create a webhook pointing to this skill with pull request events enabled.

```yaml
skills:
  - name: hacktoberfest
```

For the above configuration your webhook must point to `http(s)://host:port/skills/hacktoberfest/events`.

## Usage

When a PR is opened opsdroid will comment on it.

> user: <raises PR>
>
> opsdroid: Thanks @user! This PR counts towards Hacktoberfest so make sure you sign up.

