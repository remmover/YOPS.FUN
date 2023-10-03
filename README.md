# YOPS.FUN App

## Table of Contents

- [Introduction](#introduction)
- [Authentication](#authentication)
- [Working with Photos](#working-with-photos)
- [Commenting](#commenting)
- [Additional Features](#additional-features)
- [Emotion Analysis](#emotion-analysis)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Introduction

Welcome to the YOPS.FUN App! This application allows users to share and interact with photos in various ways. It's built using FastAPI and utilizes JWT tokens for authentication. Users can have three different roles: regular user, moderator, and administrator. The first user in the system is always an administrator.

## Authentication

Authentication is handled using JWT tokens. Users have three roles: regular user, moderator, and administrator. FastAPI decorators are used to check the token and user role for different levels of access.

## Working with Photos

Users can perform various actions related to photos, including:

- Uploading photos with descriptions (POST).
- Deleting photos (DELETE).
- Editing photo descriptions (PUT).
- Viewing a photo by its unique link (GET).
- Adding up to 5 tags per photo. Adding tags is optional when uploading a photo.
- Performing basic operations on photos using Cloudinary transformations.

## Commenting

Each photo has a comment section where users can interact by:

- Adding comments to each other's photos.
- Editing their own comments (no deletion allowed).
- Administrators and moderators can delete comments.
- Storing creation and update timestamps for comments in the database.

## Additional Features

- User profiles are accessible via a route using their unique username, displaying information such as name, registration date, and the number of uploaded photos.
- Users can edit their own profile information.
- Administrators can deactivate user accounts, preventing them from accessing the application.

## Emotion Analysis

We enhance the user experience by utilizing the OpenAI library to display emotion analysis for comments posted under photos.

## Installation

Follow these steps to set up the Photo Sharing App locally:

1. Clone the repository.
2. Install the required dependencies.
3. Configure your database settings.
4. Set up Cloudinary credentials.
5. Start the FastAPI server.

## Usage

1. Register an account or log in.
2. Start uploading, viewing, and interacting with photos.
3. Explore user profiles and update your own.
4. Admins can manage users and comments.



## License

This project is licensed under the [MIT License](link_to_license).
