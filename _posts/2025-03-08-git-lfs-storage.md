---
layout: post
title: Git Large File Storage (LFS) - How to Manage Large Files in Git
author: denzilferreira
excerpt: >
  Working with containers, images, and other large files (> 100MB) in Git can be a challenge. Git Large File Storage (LFS) is a great solution for managing large files in Git repositories. Learn how to set up and use Git LFS in your projects.
tags:
  - Git
  - Large File Storage
  - GitHub
---

## Motivation

I was working on a project that involved creating a Go application using GoCV and YOLO for object detection. The project required me to store large YOLO weights files (`.weights`) in the Git repository. The weights files were over 200MB, and pushing them to the repository did not work as the repo is configured with a 100MB file limit. I had to find a solution to manage large files in Git repositories.

This led me to learn about Git Large File Storage (LFS). You can use Git LFS to avoid bloating the repository with large files. Large files can slow down cloning and fetching operations, especially for team members with limited bandwidth.

## What is Git LFS?

Git Large File Storage (LFS) is an open-source Git extension that replaces large files in your repository with text pointers. The actual large files are stored on a remote server, such as GitHub, GitLab, or Bitbucket. Git LFS is designed to work transparently with Git, so you can continue using Git commands as usual. If your project is on GitHub, the files will be stored in the GitHub LFS storage by default.

## Setting Up Git LFS

To use Git LFS, you need to install the Git LFS client on your machine. You can download the client from the [Git LFS website](https://git-lfs.com). After installing the client, you need to enable Git LFS in your repository.

To enable Git LFS in your repository, run the following command:

```sh
git lfs install
```

This command initializes Git LFS in your repository and sets up the necessary hooks. You can now start tracking large files using Git LFS.

## Using Git LFS

To start tracking large files with Git LFS, you need to specify the file extensions or file names that you want to track. You can do this by running the following command:

```sh
git lfs track "*.zip"
```

This will tell Git LFS to track all files with the `.zip` extension. You can specify multiple files using a comma-separated list:

```sh
git lfs track "*.zip, *.tar.gz, *.weights"
```

You can also specify individual files. In my case, I only needed to store one large file, the YOLO weights file:

```sh
git lfs track "models/yolov3.weights"
```

Git LFS will create a `.gitattributes` file in your repository that contains the tracking information. You will need to commit this file to your repository to start tracking large files with Git LFS.

You can confirm that Git LFS is tracking the files by running the following command:

```sh
git lfs ls-files
> 523e4e69e1 * models/yolov3.weights
```

Behind the scenes, Git LFS replaces the large files with text pointers in your repository. The actual large files will be uploaded and stored on the remote server when you push.

## Pushing the changes and store the Large Files

We can now push the `.gitattributes` file to the repository and push the large files to the remote server. To push the changes to the remote server, run the following commands:

```sh
git add .gitattributes models/yolov3.weights
git commit -m "Add YOLO weights file using Git LFS"
git push origin main
```

This will push the `.gitattributes` file and the YOLO weights file to the remote server. The actual large file will be stored in the Git LFS storage, and the text pointer will be stored in the repository.

## Reverse the process to retrieve the Large Files

When you clone the repository to your machine, you will need to run the following command to download the large files:

```sh
git lfs pull
```

This command will download the large files from the Git LFS storage and replace the text pointers in your repository with the actual large files.

## Conclusion

Git Large File Storage (LFS) is a great solution for managing large files in Git repositories. It allows you to avoid bloating the repository with large files and improves the performance of cloning and fetching operations. If you are working with large files in Git, I highly recommend using Git LFS to manage them effectively.

## References
- [Git LFS](https://git-lfs.com)
- [GitHub LFS Documentation](https://docs.github.com/en/repositories/working-with-files/managing-large-files/configuring-git-large-file-storage)