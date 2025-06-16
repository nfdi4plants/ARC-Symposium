# arc-processes2mermaid

## add solution

```bash
dotnet new sln --name arc-processes2mermaid
dotnet new console -lang "F#" -o src/arc-processes2mermaid
dotnet sln add src/arc-processes2mermaid/arc-processes2mermaid.fsproj
dotnet new gitignore
```

## add dependencies

```bash
cd src/arc-processes2mermaid/
dotnet add package Argu
dotnet add package ARCtrl.NET -v 1.1.0
dotnet add package ARCtrl.QueryModel -v 1.0.5
cd ../../
```

## build project

```bash
dotnet build src/arc-processes2mermaid/arc-processes2mermaid.fsproj
```

## start app

```bash
src/arc-processes2mermaid/bin/Debug/net8.0/arc-processes2mermaid --help
```

## local test

```bash
src/arc-processes2mermaid/bin/Debug/net8.0/arc-processes2mermaid -a ~/datahub-dataplant/hhu-plant-biochemistry/Samuilov-2018-BOU-PSP
```

## create self-contained executable

### for macos

```bash
dotnet publish --runtime osx-x64 -p:PublishReadyToRunShowWarnings=true -p:PublishSingleFile=true
```
