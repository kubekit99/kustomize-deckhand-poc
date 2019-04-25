# TransformerConfig syntax

```go
type TransformerConfig struct {
	NamePrefix        fsSlice  `json:"namePrefix,omitempty" yaml:"namePrefix,omitempty"`
	NameSuffix        fsSlice  `json:"nameSuffix,omitempty" yaml:"nameSuffix,omitempty"`
	NameSpace         fsSlice  `json:"namespace,omitempty" yaml:"namespace,omitempty"`
	CommonLabels      fsSlice  `json:"commonLabels,omitempty" yaml:"commonLabels,omitempty"`
	CommonAnnotations fsSlice  `json:"commonAnnotations,omitempty" yaml:"commonAnnotations,omitempty"`
	NameReference     nbrSlice `json:"nameReference,omitempty" yaml:"nameReference,omitempty"`
	VarReference      fsSlice  `json:"varReference,omitempty" yaml:"varReference,omitempty"`
	Images            fsSlice  `json:"images,omitempty" yaml:"images,omitempty"`
}
```

```go
type Gvk struct {
	Group   string `json:"group,omitempty" yaml:"group,omitempty"`
	Version string `json:"version,omitempty" yaml:"version,omitempty"`
	Kind    string `json:"kind,omitempty" yaml:"kind,omitempty"`
}
```

```go
type FieldSpec struct {
	gvk.Gvk            `json:",inline,omitempty" yaml:",inline,omitempty"`
	Path               string `json:"path,omitempty" yaml:"path,omitempty"`
	CreateIfNotPresent bool   `json:"create,omitempty" yaml:"create,omitempty"`
}

type fsSlice []FieldSpec
```

```go
type NameBackReferences struct {
	gvk.Gvk    `json:",inline,omitempty" yaml:",inline,omitempty"`
	FieldSpecs fsSlice `json:"FieldSpecs,omitempty" yaml:"FieldSpecs,omitempty"`
}

type nbrSlice []NameBackReferences
```
