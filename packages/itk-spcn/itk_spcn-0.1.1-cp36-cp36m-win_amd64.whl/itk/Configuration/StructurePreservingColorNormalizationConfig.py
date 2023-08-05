depends = ('ITKPyBase', 'ITKStatistics', 'ITKImageSources', 'ITKCommon', )
templates = (
  ('StructurePreservingColorNormalizationFilter', 'itk::StructurePreservingColorNormalizationFilter', 'itkStructurePreservingColorNormalizationFilterIRGBUC2', True, 'itk::Image< itk::RGBPixel< unsigned char >,2 >'),
  ('StructurePreservingColorNormalizationFilter', 'itk::StructurePreservingColorNormalizationFilter', 'itkStructurePreservingColorNormalizationFilterIRGBUC3', True, 'itk::Image< itk::RGBPixel< unsigned char >,3 >'),
  ('StructurePreservingColorNormalizationFilter', 'itk::StructurePreservingColorNormalizationFilter', 'itkStructurePreservingColorNormalizationFilterIRGBAUC2', True, 'itk::Image< itk::RGBAPixel< unsigned char >,2 >'),
  ('StructurePreservingColorNormalizationFilter', 'itk::StructurePreservingColorNormalizationFilter', 'itkStructurePreservingColorNormalizationFilterIRGBAUC3', True, 'itk::Image< itk::RGBAPixel< unsigned char >,3 >'),
  ('StructurePreservingColorNormalizationFilter', 'itk::StructurePreservingColorNormalizationFilter', 'itkStructurePreservingColorNormalizationFilterIVF32', True, 'itk::Image< itk::Vector< float,3 >,2 >'),
  ('StructurePreservingColorNormalizationFilter', 'itk::StructurePreservingColorNormalizationFilter', 'itkStructurePreservingColorNormalizationFilterIVF33', True, 'itk::Image< itk::Vector< float,3 >,3 >'),
  ('StructurePreservingColorNormalizationFilter', 'itk::StructurePreservingColorNormalizationFilter', 'itkStructurePreservingColorNormalizationFilterIVF42', True, 'itk::Image< itk::Vector< float,4 >,2 >'),
  ('StructurePreservingColorNormalizationFilter', 'itk::StructurePreservingColorNormalizationFilter', 'itkStructurePreservingColorNormalizationFilterIVF43', True, 'itk::Image< itk::Vector< float,4 >,3 >'),
  ('StructurePreservingColorNormalizationFilter', 'itk::StructurePreservingColorNormalizationFilter', 'itkStructurePreservingColorNormalizationFilterICVF32', True, 'itk::Image< itk::CovariantVector< float,3 >,2 >'),
  ('StructurePreservingColorNormalizationFilter', 'itk::StructurePreservingColorNormalizationFilter', 'itkStructurePreservingColorNormalizationFilterICVF33', True, 'itk::Image< itk::CovariantVector< float,3 >,3 >'),
  ('StructurePreservingColorNormalizationFilter', 'itk::StructurePreservingColorNormalizationFilter', 'itkStructurePreservingColorNormalizationFilterICVF42', True, 'itk::Image< itk::CovariantVector< float,4 >,2 >'),
  ('StructurePreservingColorNormalizationFilter', 'itk::StructurePreservingColorNormalizationFilter', 'itkStructurePreservingColorNormalizationFilterICVF43', True, 'itk::Image< itk::CovariantVector< float,4 >,3 >'),
  ('StructurePreservingColorNormalizationFilter', 'itk::StructurePreservingColorNormalizationFilter', 'itkStructurePreservingColorNormalizationFilterVIUC2', True, 'itk::VectorImage< unsigned char,2 >'),
  ('StructurePreservingColorNormalizationFilter', 'itk::StructurePreservingColorNormalizationFilter', 'itkStructurePreservingColorNormalizationFilterVIUC3', True, 'itk::VectorImage< unsigned char,3 >'),
  ('StructurePreservingColorNormalizationFilter', 'itk::StructurePreservingColorNormalizationFilter', 'itkStructurePreservingColorNormalizationFilterVIUS2', True, 'itk::VectorImage< unsigned short,2 >'),
  ('StructurePreservingColorNormalizationFilter', 'itk::StructurePreservingColorNormalizationFilter', 'itkStructurePreservingColorNormalizationFilterVIUS3', True, 'itk::VectorImage< unsigned short,3 >'),
  ('StructurePreservingColorNormalizationFilter', 'itk::StructurePreservingColorNormalizationFilter', 'itkStructurePreservingColorNormalizationFilterVIF2', True, 'itk::VectorImage< float,2 >'),
  ('StructurePreservingColorNormalizationFilter', 'itk::StructurePreservingColorNormalizationFilter', 'itkStructurePreservingColorNormalizationFilterVIF3', True, 'itk::VectorImage< float,3 >'),
  ('StructurePreservingColorNormalizationFilter', 'itk::StructurePreservingColorNormalizationFilter', 'itkStructurePreservingColorNormalizationFilterVID2', True, 'itk::VectorImage< double,2 >'),
  ('StructurePreservingColorNormalizationFilter', 'itk::StructurePreservingColorNormalizationFilter', 'itkStructurePreservingColorNormalizationFilterVID3', True, 'itk::VectorImage< double,3 >'),
)
snake_case_functions = ('structure_preserving_color_normalization_filter', )
