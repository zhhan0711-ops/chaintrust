# Security policy

## Supported status

ChainTrust is an early-stage engineering review tool. It is not a professional security audit service and does not provide a security guarantee for reviewed contracts.

## Reporting a vulnerability

Please do not publish exploitable security issues, credentials, or private deployment details in a public issue. Contact the maintainer through the email listed on the portfolio website and include:

- the affected component;
- reproduction steps;
- expected and observed behavior;
- potential impact;
- a suggested remediation, if available.

## Secret handling

Never commit `.env` files, private keys, RPC credentials, API keys, database URLs containing passwords, or deployed operator configuration. Example environment files must contain placeholders only.

