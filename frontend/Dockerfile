# Copyright 2025 Booz Allen Hamilton.
#
# Booz Allen Hamilton Confidential Information.
#
# The contents of this file are the intellectual property of
# Booz Allen Hamilton, Inc. ("BAH") and are subject to copyright protection
# under the laws of the United States and other countries.
#
# You acknowledge that misappropriation, misuse, or redistribution of content
# on the file could cause irreparable harm to BAH and/or to third parties.
#
# You may not copy, reproduce, distribute, publish, display, execute, modify,
# create derivative works of, transmit, sell or offer for resale, or in any way
# exploit any part of this code or program without BAH's express written permission.
#
# The contents of this code or program contains code
# that is itself or was created using artificial intelligence.
#
# To the best of our knowledge, this code does not infringe third-party intellectual
# property rights, contain errors, inaccuracies, bias, or security concerns.
#
# However, Booz Allen does not warrant, claim, or provide any implied
# or express warranty for the aforementioned, nor of merchantability
# or fitness for purpose.
#
# Booz Allen expressly limits liability, whether by contract, tort or in equity
# for any damage or harm caused by use of this artificial intelligence code or program.
#
# Booz Allen is providing this code or program "as is" with the understanding
# that any separately negotiated standards of performance for said code
# or program will be met for the duration of any applicable contract under which
# the code or program is provided.

FROM node:21-alpine3.19 AS base

# setup pnmp
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

ARG APP_USERNAME=appuser
ARG USER_UID=10001
ARG USER_GID=10001
ARG APP_PORT=3000

# Install dependencies only when needed
FROM base AS deps

WORKDIR /app

# Install dependencies based on the preferred package manager
COPY package.json pnpm-lock.yaml ./
RUN corepack enable pnpm && pnpm i --frozen-lockfile

# Rebuild the source code only when needed
FROM deps AS builder

WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

RUN corepack enable pnpm && pnpm run build

#####  Production image, copy all the files and run next
FROM base AS runner

# Upgrade OS packages to pull in security-related patches.
RUN apk upgrade --no-cache

# Add dumb-init in line with node.js application best-practices.
# See: https://snyk.io/blog/10-best-practices-to-containerize-nodejs-web-applications-with-docker/
RUN apk upgrade --no-cache && apk add --no-cache dumb-init

WORKDIR /app

# Create app-specific group and user.
RUN true \
  && addgroup --system --gid ${USER_GID} ${APP_USERNAME} \
  && adduser --system --uid ${USER_UID} --ingroup ${APP_USERNAME} ${APP_USERNAME}

COPY --from=builder --chown=${APP_USERNAME}:${APP_GROUPNAME} /app .

RUN chown -R ${APP_USERNAME}:${APP_USERNAME} /app

EXPOSE ${APP_PORT}

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
# TODO:
# !! We need to figure out what it looks like to have a "prod" container
# for vite. Right now, the container launches the dev server which we definitely do
# not want in production!
CMD ["pnpm", "run", "dev", "--host", "0.0.0.0", "--port", "80"]

USER ${APP_USERNAME}
